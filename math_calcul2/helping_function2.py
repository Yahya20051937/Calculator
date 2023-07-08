def get_divisor(data_structure):
    from math_calcul2.helping_function import get_parenthesis_sub_array, has_sublists
    index_counter = -1
    divisors = []  # this list will store all the divisors
    divisors = find_divisors(divisors, data_structure)
    # now after getting the big divisor, lets get the subdivisions

    for array in data_structure:
        if has_sublists(array):

            divisors = find_divisors(divisors, array)
            for sub_array in array:
                if has_sublists(sub_array):
                    divisors = find_divisors(divisors, sub_array)
    return divisors


def find_divisors(divisors, array):
    index_counter = -1
    for sub_array in array:
        index_counter += 1
        if sub_array == '/':
            sub_divisor = array[index_counter + 1]
            divisors.append(sub_divisor)
    return divisors


def get_elements_until(string, x):
    result = []
    for char in string:
        if char == x:
            break
        result.append(char)
    if len(result) == 0:
        result.append('1')
    return ''.join(result)


def get_elements_after(string, x):
    result = []
    found_x = False

    for char in string:
        if found_x:
            result.append(char)
        if char == x:
            found_x = True

    return ''.join(result)


def find_indices(lst, elements):
    indices = []
    for i in range(len(lst)):
        if lst[i] in elements:
            indices.append(i)
    return indices


def move_first_two_to_end(lst):
    if len(lst) >= 2:
        lst.append(lst.pop(0))
        lst.append(lst.pop(0))
    return lst


def check_if_string_with_x(str1, str2):
    str1, str2 = str(str1), str(str2)
    if 'x' in str1 and 'x' in str2:
        return True, True
    elif 'x' in str1:
        return True, False
    elif 'x' in str2:
        return False, True
    else:
        return False, False


def check_conditions(inside_function):
    if isinstance(inside_function, list):
        if 'x' not in inside_function:
            return True
        else:
            return False
    else:
        return True


def transform_array(new_array, result, signs, skip_next, add_to_skip_next):
    try:
        if len(new_array) != 0 or new_array[-1] in signs:
            new_array += [result]
        else:
            new_array += ['+'] + [str(result)]
    except IndexError:
        new_array += ['+'] + [str(result)]
    skip_next += add_to_skip_next
    return new_array, skip_next


def check_if_inside_parenthesis(array, element_position):
    condition1 = False
    condition2 = False
    closing_parenthesis_position = None  # this variable will be used later
    # an element is inside parenthesis if after the element position there is a ')' and no '(' between the closing bracket position and the element position and before the element position there is a '(' and no  ')' between the opening parenthesis and the element position
    index_counter = element_position - 1
    for element in array[element_position:]:
        index_counter += 1
        if element == ')':
            # check if there is no opening bracket between the element position and the closing bracket
            if '(' not in array[element_position:index_counter]:
                condition1 = True
                closing_parenthesis_position = index_counter
                break

    index_counter = 0
    for element in array[:element_position]:
        index_counter += 1
        if element == '(':
            if ')' not in array[index_counter:element_position]:
                condition2 = True
                break

    if condition1 and condition2:
        return True, closing_parenthesis_position
    else:
        return False, closing_parenthesis_position


def check_element_after_condition(array, last_index):
    try:
        if array[last_index + 1] != '^':
            return True
        else:
            return False
    except IndexError:
        return True


def brackets_algorithm(array, index_counter, to_calculate=False,
                       variable=False):  # the third argument will say if we have to calculate what it inside the brackets or not
    from math_calcul2.organizing_function import organize_calcul_list
    j = 0
    index_counter2 = index_counter
    for next_element in array[index_counter + 1:]:
        index_counter2 += 1
        if next_element == '(':
            j += 1
        elif next_element == ')':
            j -= 1
            if j < 0:
                sub_array = array[index_counter + 1:index_counter2]
                ln_sub_array = len(sub_array)

                sub_array = organize_calcul_list(sub_array, variable=variable,
                                                 to_calculate=to_calculate,
                                                 recursive=True)  # organize the expression inside the brackets
                return sub_array, ln_sub_array, index_counter2


def reverse_brackets_algorithm(array, index_counter, to_calculate=False, variable=False):
    from math_calcul2.organizing_function import organize_calcul_list
    j = 0
    index = index_counter
    while j >= 0:
        index -= 1
        if array[index] == ')':
            j += 1
        elif array[index] == '(':
            j -= 1

    sub_array = array[index + 1:index_counter]
    ln_sub_array = len(sub_array)

    sub_array = organize_calcul_list(sub_array, variable=variable,
                                                 to_calculate=to_calculate,
                                                 recursive=True)  # organize the expression inside the brackets
    return sub_array, ln_sub_array, index

