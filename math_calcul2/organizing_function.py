import math

from math_calcul2.helping_function import get_parenthesis_sub_array, get_sub_array2, has_common_items, \
    turn_elements_to_None, \
    check_pattern, split_array, process_list

from Errors.errors_handling import brackets_handling, signs_handling


@brackets_handling
@signs_handling
def organize_calcul_list(array, to_calculate=True, variable=False, recursive=False):
    from math_calcul2.calculating_function import calculate1
    from functions.my_functions import replace_sequence_in_array
    from math_calcul2.helping_function import has_sublists, handle_minus

    new_array = []

    new_array = organize_numbers(array, new_array, recursive)
    new_array = organize_math_function(new_array, [])
    new_array = organize_power(new_array, [])
    new_array = organize_parenthesis(new_array, [], variable)
    new_array1 = []
    if has_sublists(new_array):
        for arr in new_array:
            if arr.__class__ == list and not has_common_items(arr, ['ln', 'exp', 'cos', 'sin', 'tan', 'sqrt']):

                new_arr = organize_parenthesis(arr, [])

                new_arr = organize_signs_(new_arr, [])
                new_array1.append(new_arr)
            else:
                new_array1.append(arr)

        new_array = new_array1

    new_array = organize_signs_(new_array, [])

    if new_array[0] == '+':
        new_array = new_array[1:]

    if to_calculate and not variable:
        result = calculate1(new_array)
        return result
        # if the function is used to organize a sub_array then the calcul will be done later
    elif variable:
        new_array = calculate1(new_array, variable=True)
        return new_array
    else:
        return new_array


def organize_parenthesis(array, new_array, variable=False):
    """
    The algorithm is, for each opening bracket, set a variable tha will be incremented whenever it encounters an opening bracket and will be decremented whenever
     it encounters a closing bracket, and when j is less than zero, we found the corresponded closing bracket

    """
    from math_calcul2.helping_function2 import brackets_algorithm

    signs = ('+', '-')
    signs2 = ('*', '/')

    skip_next = 0
    index_counter = -1
    for element in array:
        index_counter += 1

        if skip_next > 0:
            skip_next -= 1
            continue

        if element == '(':
            sub_array, ln_sub_array, index = brackets_algorithm(array, index_counter,
                                                                variable=variable)  # here we implement the algorithm
            if sub_array[0] == '-':
                sub_array = [0] + sub_array  # add a zero to the beginning of the list for logic purposes

            if array[index_counter - 1] in signs or array[index_counter - 1] in signs2:
                new_array += [
                    sub_array]  # check if I have to add a plus sign or not (if the ( is the first element in the list)
            else:
                new_array += ['+'] + [sub_array]

            skip_next += ln_sub_array + 1


        else:
            new_array += [element]
    if new_array[0] == '+':
        new_array = new_array[1:]

    return new_array


def organize_signs_(array, new_array):
    signs = ('+', '-')
    signs2 = ('*', '/')
    skip_next = 0
    if has_common_items(array, signs):
        for i in range(len(array)):
            if skip_next > 0:
                skip_next -= 1
                continue
            if array[i] in signs:

                sub_array1 = [j for j in array[:i] if j is not None]

                sub_array1_ln = len(sub_array1)

                if sub_array1_ln == 0:
                    sub_array1 = [0]  # this will be used to replace the empty list with a 0 in it for logical purposes
                    sub_array1_ln = 1

                sub_array2, index = get_sub_array2(array, i)
                try:
                    sub_array2_len = len(sub_array2)
                except TypeError:
                    sub_array2_len = len(array[
                                         i + 1:])  # the variable will be used to elements to None because the next line may modify the real length
                sub_array1, sub_array2 = process_list(sub_array1), process_list(sub_array2)
                if sub_array2 is None:  # if this index represents the last sing in this array

                    sub_array2 = process_list(array[i + 1:])

                    if sub_array1_ln == 0:
                        new_array += [array[i]] + [sub_array2]  # add all the elements in the array as the second item
                        skip_next += len(array[i + 1:])

                    else:
                        new_array += [sub_array1] + [array[i]] + [sub_array2]
                        skip_next += len(array[i + 1:])
                    array = turn_elements_to_None(array, i, len(array) - 1)
                else:
                    skip_next += sub_array2_len
                    if sub_array1_ln != 0:
                        new_array += [sub_array1] + [array[i]] + [sub_array2]
                    else:
                        new_array += [array[i]] + [sub_array2]
                    if i >= sub_array1_ln:
                        array = turn_elements_to_None(array, i - sub_array1_ln, i + sub_array2_len)
                    else:
                        array = turn_elements_to_None(array, 0, i + sub_array2_len)

                    continue
        return new_array
    else:
        return array


def organize_math_function(array, new_array):
    from math_calcul2.calculating_function import calculate_func_sub_array
    from math_calcul2.helping_function2 import brackets_algorithm

    functions = ['ln', 'exp', 'cos', 'sin', 'tan', 'sqrt']
    signs = ('+', '-')
    skip_next = 0
    for i in range(len(array)):
        if skip_next > 0:
            skip_next -= 1
            continue
        if array[i] in functions:
            inside_function, ln_inside_function, index = brackets_algorithm(array, i + 1, to_calculate=True)

            function = [array[i]] + ['('] + [inside_function] + [')']
            ln_function = len(function)
            # let's calculate the function here if it is calculable
            if 'x' not in function:
                function = calculate_func_sub_array(function)
            # array = turn_elements_to_None(array, i, index + 1 + i)
            try:
                if len(new_array) != 0 or new_array[-1] in signs:

                    new_array += [function]
                else:
                    new_array += ['+'] + [function]
            except IndexError:

                new_array += ['+'] + [function]
            skip_next += ln_function - 1
        else:
            new_array += [array[i]]
            array[i] = None
    if new_array[0] == '+':
        new_array = new_array[1:]
    return new_array


def organize_power(array, new_array):
    from math_calcul2.calculating_function import calculate1
    from math_calcul2.helping_function2 import transform_array, check_if_inside_parenthesis, \
        check_element_after_condition, brackets_algorithm, reverse_brackets_algorithm
    skip_next = 0
    signs = ('+', '-')
    for i in range(len(array)):
        if skip_next > 0:
            skip_next -= 1
            continue
        # we have to look for this symbol and check if the element after is a number, or it is an opening parenthesis
        if array[i] == '^':
            if array[i + 1] != '(':  # '[' is prohibited here !! (add it in the app limitations)
                # handle the case where the power is a number and not an expression
                # also, the element before should either be a number or an expression
                if array[i - 1] != ')':
                    # handle the case where the thing raised to the power is a number
                    result = float(array[i - 1]) ** float(array[i + 1])
                    new_array, skip_next = transform_array(new_array, result, signs, skip_next, 2)
                else:
                    # handle the case where the thing raised to the power is an expression
                    expression_raised_to_power, length, index = reverse_brackets_algorithm(array, i-1)

                    if 'x' not in expression_raised_to_power:
                        expression_raised_to_power = organize_calcul_list(expression_raised_to_power)

                        result = expression_raised_to_power ** float(array[i + 1])

                        new_array, skip_next = transform_array(new_array, result, signs, skip_next, 2)
            else:
                # handle the case where the thing raised to the power is an expression
                if array[i - 1] != ')':
                    # handle the case where the expression raised to the power is not a number
                    power_expression,len_power_expression, index = brackets_algorithm(array, i + 1)

                    if 'x' not in power_expression:
                        power_expression = organize_calcul_list(power_expression)
                        result = float(array[i - 1]) ** power_expression
                        new_array, skip_next = transform_array(new_array, result, signs, skip_next,
                                                               len_power_expression + 1)
                else:
                    # handle the case where the thing raised to the power is an expression
                    expression_raised_to_power, length, index = reverse_brackets_algorithm(array, i - 1)
                    if 'x' not in expression_raised_to_power:
                        expression_raised_to_power = organize_calcul_list(expression_raised_to_power)

                    power_expression, ln_power_expression, index = brackets_algorithm(array, i + 1)

                    if 'x' not in power_expression:
                        power_expression = organize_calcul_list(power_expression)

                    result = expression_raised_to_power ** power_expression
                    new_array, skip_next = transform_array(new_array, result, signs, skip_next, ln_power_expression + 1)
        else:
            inside_parenthesis_bool, closing_parenthesis_index = check_if_inside_parenthesis(array, i)
            # we can only add elements in the new array if the element is not inside parenthesis and element after != ^ or if the element is inside parenthesis and the element after ) != ^
            # there is also a case where the element is a parenthesis symbol
            if inside_parenthesis_bool is True:
                # check if the element after the parenthesis expression is a power symbol
                if check_element_after_condition(array, closing_parenthesis_index):
                    new_array += [array[i]]
                    array[i] = None
            else:
                if array[i] == '(':
                    # we first must get the closing bracket position, and check if after it there is a ^ or not
                    closing_bracket_index = brackets_algorithm(array, i)[2]
                    if check_element_after_condition(array, closing_bracket_index):
                        new_array += [array[i]]
                        array[i] = None

                elif array[i] == ')':  # we must add if the element after this position is not ^
                    if check_element_after_condition(array, i):
                        new_array += [array[i]]
                        array[i] = None
                else:
                    # handle the case where the element is a number
                    if check_element_after_condition(array, i):
                        new_array += [array[i]]
                        array[i] = None
    if new_array[0] == '+':
        new_array = new_array[1:]

    return new_array


def organize_numbers(array, new_array, recursive=False):
    # if two numbers are not separated by anything, then they form the same number
    if recursive:  # if the function call is recursive, we don't need to run this function
        return array
    index_counter = -1
    skip_next = 0
    numbers = range(10)
    numbers2 = [str(n) for n in numbers]
    for element in array:
        index_counter += 1
        if skip_next > 0:
            skip_next -= 1
            continue

        if element in numbers or element in numbers2:  # if the element is a number, we loop while the next element is a number, and we gather all the numbers in the variable number
            number = str(element)
            j = index_counter
            try:
                while array[j + 1] in numbers or array[j + 1] in numbers2:
                    number += str(array[j + 1])
                    j += 1
            except IndexError:
                pass
            new_array += [int(float(number))]
            skip_next += len(number) - 1
        else:
            new_array += [element]

    if new_array[0] == '+':
        new_array = new_array[1:]

    return new_array
