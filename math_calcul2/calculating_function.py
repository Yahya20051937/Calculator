import math
from math_calcul2.helping_function import has_common_items, get_sub_array2, check_pattern, has_sublists, \
    get_parenthesis_sub_array, \
    process_list
from math_calcul2.distributing_function import is_calculable, is_calculable2

funcs = ['ln', 'exp', 'cos', 'sin', 'tan', 'sqrt']
signs = ('+', '-')
signs2 = ('*', '/')

math_functions = {
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "ln": math.log,
    "exp": math.exp,

}


def calculate1(big_array, variable=False):
    if not has_sublists(big_array):
        if has_common_items(big_array, signs):
            big_array = calculate_normal_sub_array(big_array)
            return big_array
        elif has_common_items(big_array, signs2):
            big_array = calculate_normal_sub_array2(big_array)
            return big_array
        else:
            return big_array[0]
            # if both conditions are false then the big_array has only one item
    else:
        index_counter_0 = -1
        for array in big_array:
            big_array, index_counter_0 = handle_array(array, index_counter_0, big_array, variable)

    return calculate2(big_array, variable)  # now calculate the arrays


def handle_array(array, index_counter_0, big_array, variable=False):
    index_counter_0 += 1
    if array.__class__ == list:
        if has_sublists(array):

            if not has_common_items(array, funcs):
                index_counter = -1
                for sub_array in array:

                    index_counter += 1
                    if sub_array.__class__ == list:
                        if not has_common_items(sub_array, funcs):
                            array[index_counter] = calculate_normal_sub_array(sub_array)
                        else:
                            array[index_counter] = calculate_func_sub_array(sub_array, variable)

            else:
                big_array[index_counter_0] = calculate_func_sub_array(array, variable)
        else:
            if has_common_items(array, funcs):
                big_array[index_counter_0] = calculate_func_sub_array(array, variable)
            elif has_common_items(array, signs):
                big_array[index_counter_0] = calculate_normal_sub_array(array)
    return big_array, index_counter_0


@is_calculable
def calculate_normal_sub_array(sub_array):  # this function expects a pattern like this e.g., number, operator, number)
    from math_calcul2.helping_function2 import move_first_two_to_end
    index_counter = -1
    result = 0
    skip_next = 0
    if len(sub_array) == 1:
        return float(sub_array[0])

    if sub_array[0] == '-':
        sub_array = move_first_two_to_end(sub_array)

    if sub_array[0] == '+':
        sub_array = sub_array[1:]

    first_calculation = True  # this variable will be used to check if I have to add the previous item to that calculation or if it is already calculated

    for num in sub_array:
        index_counter += 1

        if skip_next > 0:
            skip_next -= 1
            first_calculation = False  # if the element is skipped then the first calculation has already been made
            continue

        if num == '+':
            result = make_calculation(True, sub_array, index_counter, result,
                                      first_calculation)  # true refers to the plus sign
            skip_next += 1
        elif num == '-':
            result = make_calculation(False, sub_array, index_counter, result,
                                      first_calculation)  # false refers to the minus sign
            skip_next += 1

    return result


def make_calculation(sign, sub_array, index_counter, result, first_calculation):
    from math_calcul2.helping_function import handle_item
    from math_calcul2.helping_function2 import check_if_string_with_x
    from math_calcul2.distributing_function import math_distribution, UnknownNumber
    if first_calculation:
        item1 = sub_array[index_counter - 1]
        item2 = sub_array[index_counter + 1]

        item1, item2 = handle_item(item1), handle_item(
            item2)  # this line is for fixing bugs if trying to add a number and a function by getting the result of the function
        try:
            if sign:
                result += float(item1) + float(item2)
            else:
                result += float(item1) - float(item2)
        except ValueError or TypeError:
            item1_is_unknown, item2_is_unknown = check_if_string_with_x(str(item1), str(item2))
            if item1_is_unknown and not item2_is_unknown:
                unknown = UnknownNumber(str(item1))
                value = UnknownNumber(unknown.add(str(item2), sign))
            elif not item1_is_unknown and item2_is_unknown:
                unknown = UnknownNumber(str(item2))
                value = UnknownNumber(unknown.add(str(item1), sign))
            elif item1_is_unknown and item2_is_unknown:
                unknown1 = UnknownNumber(str(item1))
                unknown2 = UnknownNumber(str(item2))
                value = UnknownNumber(unknown1.add(unknown2.char,
                                                   sign))  # after adding the two items, now I have to add the sum to the result
            result = value.add(str(result), True)  # the sign is always true here
    else:
        item = sub_array[index_counter + 1]
        try:
            if sign:
                result += float(item)
            else:
                result -= float(item)
        except ValueError or TypeError:
            result = UnknownNumber(item).add(result, sign)

    return result


def calculate_func_sub_array(sub_array, variable=False):
    from math_calcul2.organizing_function import organize_signs_, organize_parenthesis
    from math_calcul2.helping_function2 import check_conditions
    inside_function = get_parenthesis_sub_array(sub_array, 1, ('(', ')'))[0]
    inside_function = organize_parenthesis(inside_function, [], ('{', '}'))
    inside_function = organize_signs_(inside_function, [])
    inside_function = calculate1(inside_function)
    if check_conditions(inside_function):
        inside_function = float(inside_function)
        if sub_array[0] in funcs[2:4]:
            inside_function *= math.pi / 180
        result = math_functions[sub_array[0]](inside_function)
        return result
    return [sub_array[0]] + ['('] + [inside_function] + [')']


def calculate2(big_array,
               variable=False):
    from math_calcul2.distributing_function import \
        redistribute  # this function expects a list of products or division separated by plus or minus
    index_counter = -1
    for array in big_array:
        index_counter += 1
        if array.__class__ == list:
            big_array[index_counter] = calculate_normal_sub_array2(array)
    if not variable:
        return calculate1(big_array)  # Now calculate the array after getting rid of the sublist s
    else:
        return redistribute(big_array)


@is_calculable2
def calculate_normal_sub_array2(sub_array):  # this function expects a pattern like this e.g., number, operator, number)
    index_counter = -1
    result = 0
    skip_next = 0

    first_calculation = True  # this variable will be used to check if I have to add the previous item to that calculation or if it is already calculated

    for num in sub_array:
        index_counter += 1

        if skip_next > 0:
            skip_next -= 1
            first_calculation = False  # if the element is skipped then the first calculation has already been made
            continue

        if num == '*':
            result = make_calculation2(True, sub_array, index_counter, result,
                                       first_calculation)  # true refers to the multiplication sign
            skip_next += 1
        elif num == '/':
            result = make_calculation2(False, sub_array, index_counter, result,
                                       first_calculation)  # false refers to the division sign
            skip_next += 1

    return result


def make_calculation2(sign, sub_array, index_counter, result, first_calculation):
    from math_calcul2.helping_function2 import check_if_string_with_x
    from math_calcul2.distributing_function import math_distribution
    if first_calculation:
        item1 = sub_array[index_counter - 1]
        item2 = sub_array[index_counter + 1]
        try:
            if sign:
                result += float(item1) * float(item2)
            else:
                result += float(item1) / float(item2)
        except ValueError or TypeError:  # if one of the two items in unknown, then we must use the multiply method to make this calculation
            value = math_distribution(item1, item2, sign)[0]  # add the sign here !!!!!!!!!!!!!
            value.add(result, True)
            result = value.char

    else:
        item = sub_array[index_counter + 1]
        try:
            if sign:
                result *= float(item)
            else:
                result /= float(item)
        except ValueError or TypeError:
            result = math_distribution(item, result, sign)[0].char
    return result
