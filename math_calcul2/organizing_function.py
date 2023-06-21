from math_calcul2.helping_function import get_parenthesis_sub_array, get_sub_array2, has_common_items, \
    turn_elements_to_None, \
    check_pattern, split_array, process_list


def organize_calcul_list(array, to_calculate=True, variable=False):
    from math_calcul2.calculating_function import calculate1
    from math_calcul2.helping_function import has_sublists

    if '[' not in array:
        new_array = []

        new_array = organize_math_function(array, new_array)
        new_array = organize_power(new_array, [])
        new_array = organize_parenthesis(new_array, [], ('(', ')'))
        new_array1 = []
        if has_sublists(new_array):
            for arr in new_array:
                if arr.__class__ == list and not has_common_items(arr, ['ln', 'exp', 'cos', 'sin', 'tan', 'sqrt']):
                    new_arr = organize_parenthesis(arr, [], ('(', ')'))
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

    else:  # get the first array and the second array and run the function on each one of them
        starting_index = 0
        all_new_sub_arrays = []
        while starting_index < len(array):
            # loop while the starting index is less than the length and run this function over each sub_array
            sub_array, next_starting_index = split_array(array, starting_index)
            if sub_array is None:
                break
            else:
                new_sub_array = organize_calcul_list(sub_array, False)
                if not variable:
                    new_sub_array = calculate1(new_sub_array)
                else:
                    new_sub_array = calculate1(new_sub_array, variable)
                all_new_sub_arrays.append(new_sub_array)

                try:
                    all_new_sub_arrays.append(array[starting_index + next_starting_index + 1])
                except IndexError:
                    pass
                starting_index += next_starting_index  # calculate each sub_array
        if not variable:
            result = calculate1(all_new_sub_arrays)
            return result
        else:  #
            result = calculate1(all_new_sub_arrays, variable)
            return result


def organize_parenthesis(array, new_array, para_type):
    signs = ('+', '-')
    signs2 = ('*', '/')
    skip_next = 0
    for i in range(len(array)):
        if skip_next > 0:
            skip_next -= 1
            continue
        if array[i] == para_type[0]:  # check if the element is a (
            sub_array, index = get_parenthesis_sub_array(array, i, para_type)  # get all the elements until the )
            if array[i - 1] in signs or array[i - 1] in signs2:
                new_array += [
                    sub_array]  # check if I have to add a plus sign or not (if the ( is the first element in the lidt)
            else:
                new_array += ['+'] + [sub_array]
            array = turn_elements_to_None(array, i,
                                          index + i)  # turn all the elements that are analyzed to None to prevent logical errors
            skip_next += len(sub_array)  # skip the element analyzed in the for loop

        else:
            if array[i] is not None:
                new_array += [array[i]]

            continue
    if new_array[0] in signs:
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

    functions = ['ln', 'exp', 'cos', 'sin', 'tan', 'sqrt']
    signs = ('+', '-')
    skip_next = 0
    for i in range(len(array)):
        if skip_next > 0:
            skip_next -= 1
            continue
        if array[i] in functions:
            inside_function, index = get_parenthesis_sub_array(array, i + 1, ('(', ')'))

            function = [array[i]] + ['('] + inside_function + [')']
            ln_function = len(function)
            # let's calculate the function here if it is calculable
            if 'x' not in function:
                function = calculate_func_sub_array(function)
            array = turn_elements_to_None(array, i, index + 1 + i)
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
        check_element_after_condition
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
                    expression_raised_to_power = get_parenthesis_sub_array(array, i - 1, ('(', ')'), reverse=True)

                    if 'x' not in expression_raised_to_power:
                        expression_raised_to_power = organize_calcul_list(expression_raised_to_power)

                        result = expression_raised_to_power ** float(array[i + 1])

                        new_array, skip_next = transform_array(new_array, result, signs, skip_next, 2)
            else:
                # handle the case where the thing raised to the power is an expression
                if array[i - 1] != ')':
                    # handle the case where the expression raised to the power is not a number
                    power_expression, index = get_parenthesis_sub_array(array, i + 1, ('(', ')'))
                    len_power_expression = len(power_expression)

                    if 'x' not in power_expression:
                        power_expression = organize_calcul_list(power_expression)
                        result = float(array[i - 1]) ** power_expression
                        new_array, skip_next = transform_array(new_array, result, signs, skip_next,
                                                               len_power_expression + 1)
                else:
                    # handle the case where the thing raised to the power is an expression
                    expression_raised_to_power = get_parenthesis_sub_array(array, i - 1, ('(', ')'), reverse=True)
                    if 'x' not in expression_raised_to_power:
                        expression_raised_to_power = organize_calcul_list(expression_raised_to_power)

                    power_expression, index = get_parenthesis_sub_array(array, i + 1, ('(', ')'))
                    ln_power_expression = len(power_expression)
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
                    closing_bracket_index = get_parenthesis_sub_array(array, i, ('(', ')'))[1]
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


"""array5 = ['[', '(', '5', '+', '2', ')', '*', '3', '-', 'exp', '(', '{', '2', '-', '9', '}', '*', '4', '+', '5', '*',
          '8', ')',
          ']', '/', '[', '(', '8', '-', '4', ')', '*', '3', '-', 'ln', '(', '2', ')',
          ']']

expression = ['[', '(', 'x', '+', '2x', ')', '*', 'x', '-', '8', '*', '4', '+', 'x', '*', 'ln', '(', '2', ')', ']', '/',
              '[', '(', '4', '+', 'exp', '(', '10', ')', ')', '*', 'x', '-', 'ln', '(', 'x'
              , ']']
expression2 = ['[', '(', '7', '-', '2', ')', '*', '(', '3', '+', '4', ')', '-', 'exp', '(', '2', ')', '+', 'ln', '(',
               '5', ')', ']', '/', '[', 'sqrt', '(', '16', ')', '+', '2', '*', '(', '6', '-', '3', ')', ']']
expression3 = ['[', 'sin', '(', '30', ')', '+', 'ln', '(', '100', ')', ']', '/'
    , '[', 'sqrt', '(', '25', ')', '-', 'cos', '(', '45', ')', ']']

expression4 = ['(', '3', '*', 'x', ')', '+', '(','8', '+', 'x', ')','*','x', '+', '9', '*', 'x', '-', '(', 'sqrt', '(', '9', ')', '*', '2', ')']
expression5 = ['[', '(', '3', '+', '2', ')', '*', '(', '3', '-', '1', ')', ']', '/', '[', '(', '4', '+', '1', ')', ']']
expression6 = ['[', '(', '6', '+', '2', ')', '*', '(', '9', '-', '3', ')', '+', '4', ']',
               '/', '[', '(', '5', '+', '1', ')', '*', '(', '3', '-', '2', ')', ']']

rational_function = ['[', '2', '*', 'x', '+', '1', ']', '/', '[', 'x', '-', '3', ']']


To represent the expression (5 - 1) ^ (3 + 2) as a Python list, you can use the following structure:

python
Copy code
]

print(organize_calcul_list(expression, variable=True))
"""

expression = [
    '(',
    5,
    '-',
    1,
    ')',
    '^',
    '(',
    3,
    '+',
    2,
    ')'
]
# print(organize_calcul_list(expression, variable=True))
