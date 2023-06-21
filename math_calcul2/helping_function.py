def turn_elements_to_None(array, s, f):
    for i in range(s, f + 1):
        array[i] = None
    return array


def has_common_items(list1, list2):
    return any(item in list1 for item in list2)


def get_sub_array2(array, index):
    signs = ('+', '-')
    index_counter = -1
    for element in array[index + 1:]:
        index_counter += 1
        if element in signs:
            sub_array2 = array[index + 1:index_counter + index + 1]

            return sub_array2, index_counter

    return None, None


def get_parenthesis_sub_array(array, index, para_type=('(', ')'), reverse=False):
    if not reverse:
        index_counter = -1
        for element in array[index:]:
            index_counter += 1
            if element == para_type[1]:
                sub_array = array[index + 1:index_counter + index]

                return sub_array, index_counter
    elif reverse:
        limit = index
        for i in range(limit):
            limit -= 1
            # check if this index represents '('
            if array[limit] == para_type[0]:
                sub_array = array[limit + 1: index]
                return sub_array


def check_previous_element(array, i):
    try:
        if array[i - 1].__class__ == list or array[i - 1] is None:
            return False
        else:
            return True
    except IndexError:
        pass

    return True


signs2 = ('/', '*')


def check_next_elements(array, i):
    try:
        if array[i + 1].__class__ == list and array[i + 2] not in signs2:
            return True
        else:
            return False
    except IndexError:
        pass

    return True


def check_pattern(array, i):
    if check_previous_element(array, i) and check_next_elements(array, i):
        return True

    return False


def has_sublists(lst):
    for item in lst:
        if isinstance(item, list):
            return True
    return False


def split_array(array, starting_index):
    index_counter = -1
    for element in array[starting_index:]:
        index_counter += 1
        if element == '[':
            sub_array = get_parenthesis_sub_array(array[starting_index:], index_counter, ('[', ']'))
            return sub_array[0], index_counter + sub_array[
                1]  # get all the elements until the closing bracket and the next starting index
    return None, None


def process_list(lst):
    if lst is None:
        return None
    elif len(lst) == 1:
        return lst[0]
    else:
        return lst


def handle_item(item):
    from math_calcul2.calculating_function import calculate_func_sub_array
    if item.__class__ == list:
        if has_common_items(item, ('ln', 'exp', 'cos', 'sin', 'tan', 'sqrt')):
            return calculate_func_sub_array(item)
    else:
        return item


# get_parenthesis_sub_array(['3', '+', '(', '8', '+', '2', ')'], index=6, para_type=('(', ')'), reverse=True)
