def move_to_side2_1(side1, side2, signs, variable = None):
    if variable is None:
        variable = 'x'

    index_counter = -1
    for array in side1:
        index_counter += 1
        if variable not in array and array.__class__ == list:
            if index_counter > 0:
                sign = side1[index_counter - 1]
                side1 = side1[:index_counter - 1] + side1[index_counter + 1:]
            else:
                sign = '+'
                side1 = side1[index_counter + 1:]

            side2 = side2 + [signs[sign]] + [array]

            index_counter -= 2
    index_counter = -1
    for array in side2:
        index_counter += 1
        if variable in array and array.__class__ == list:
            if index_counter > 0:
                sign = side2[index_counter - 1]
                side2 = side2[:index_counter - 1] + side1[index_counter + 1:]
            else:
                sign = '+'
                side2 = side2[index_counter + 1:]

            side1 = side1 + [signs[sign]] + [array]
            index_counter -= 2
    return side1, side2


def get_factors(side1):
    from functions.my_functions import divider_into_multiplier
    index_counter2 = -1
    all_factors = []
    for array1 in side1:
        index_counter2 += 1
        if len(array1) != 1:
            index_counter3 = -1
            for n in array1:
                index_counter3 += 1
                if n == 'x':
                    if index_counter3 + 1 != len(array1):
                        factors = array1[:index_counter3] + array1[index_counter3 + 1:]
                    else:
                        factors = array1[:index_counter3]
                    factors = divider_into_multiplier(factors)
                    if index_counter2 == 0:
                        all_factors.append(factors[:-1])
                    else:
                        sign = side1[index_counter2 - 1]
                        all_factors.append(sign)
                        all_factors.append(factors[:-1])
    return all_factors





