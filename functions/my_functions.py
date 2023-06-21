import time


def replace_sequence_in_array(sequences, array):
    possible_sequences = find_sequences(array)

    t = 0
    for f in possible_sequences:
        if f[0] in sequences:
            s_index = f[1]
            sequence = f[0]
            lim = s_index + len(sequence) - t
            array = array[:s_index - t] + [sequence] + array[lim:]
            t += len(sequence) - 1
    return array


def find_sequences(array):
    possible_sequences = []

    index_counter = -1
    for e in array:
        index_counter += 1
        element_sequences = [e]
        index = index_counter
        for i in range(1, len(array) - index):
            try:
                possible_sequence = f"{element_sequences[-1]}{array[index + i]}"

                element_sequences.append(possible_sequence)
            except IndexError:
                print(404)
        for s in element_sequences:
            possible_sequences.append((s, index))

    return possible_sequences


def set_function(x):
    function_array = [t for t in x if t != ' ']
    function_array = replace_sequence_in_array(['exp', 'ln', 'cos', 'sin', 'tan', '**'], function_array)

    for n in function_array:
        i = function_array.index(n)
        if n in [str(k) for k in range(10)]:
            function_array[i] = int(n)
            try:
                if function_array[i + 1] == 'x':
                    function_array.insert(i + 1, '*')
            except IndexError:
                pass
    return function_array


def divider_into_multiplier(factors):
    index_counter4 = -1
    for factor in factors:
        index_counter4 += 1
        if factor == '/':
            n1 = factors[index_counter4 - 1]
            n2 = 1 / factors[index_counter4 + 1]
            factors = factors[:index_counter4 - 1] + [n1, '*', n2] + factors[index_counter4 + 2:]
    return factors


def minus_array(array):
    index_counter5 = -1
    for n in array:
        condition1 = False
        condition2 = False
        index_counter5 += 1
        if n.__class__ == list and array[index_counter5 - 1] == '-':
            condition1 = True
        if index_counter5 > 1:
            if array[index_counter5 - 2].__class__ != list:
                condition2 = True
        else:
            condition2 = True
        if condition1 and condition2:
            n = [-1, '*'] + n
            if index_counter5 + 1 != len(array):
                array = array[:index_counter5 - 1] + [n] + array[index_counter5 + 1:]
            else:
                array = array[:index_counter5 - 1] + [n]

    return array


def remove_empty_arrays(arr):
    """Removes empty arrays from a given array."""
    return [a for a in arr if a]


def gather_elements(func, array):
    index_counter = -1

    for h in array:
        index_counter += 1
        if h == func:
            index_counter2 = index_counter
            for j in array[index_counter + 1:]:
                index_counter2 += 1
                if j == ')':
                    my_string = ''
                    if 'x' in array[index_counter:index_counter2 + 1]:
                        for s in array[index_counter:index_counter2 + 1]:
                            my_string += str(s)
                        array = array[:index_counter] + [my_string] + array[index_counter2 + 2:]
                        return gather_elements(func, array)

    return array
