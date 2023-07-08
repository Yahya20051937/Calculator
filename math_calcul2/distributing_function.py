from math_calcul2.helping_function2 import get_elements_until, get_elements_after


class UnknownNumber:
    def __init__(self, char='x'):
        self.char = char

    def multiply(self, n, sign, before=True):
        factor = float(get_elements_until(self.char, 'x'))
        if 'x' not in str(n):
            if sign:  # if sign evaluates to true, then we must multiply, otherwise we have to divide
                factor = n * factor
                result = f'{factor}{self.char}'  # I also have to handle the case if n = nx
            else:
                if before:
                    factor = n / factor
                    result = f'{factor}/{self.char}'
                else:
                    factor = factor / n
                    result = f'{self.char}/{factor}'
        else:
            x_index = self.char.index('x')
            try:
                if self.char[x_index + 1] != '^':
                    self.char += '^1'
            except IndexError:
                self.char += '^1'
            # this step is to avoid errors when trying to implement the math formula of powers
            x_index2 = str(n).index('x')
            try:
                if n[x_index2 + 1] != '^':
                    n += '^1'
            except IndexError:
                n += '^1'
            n_factor = get_elements_until(str(n), 'x')
            if sign:
                factor_product = float(n_factor) * float(factor)

                power1 = get_elements_after(self.char, '^')
                power2 = get_elements_after(self.char, '^')
                power_sum = float(power1) + float(power2)

            else:
                factor_product = n_factor / factor

                power1 = get_elements_after(self.char, '^')
                power2 = get_elements_until(self.char, '^')
                power_sum = float(power1) - float(power2)
            result = f"{factor_product}x^{power_sum}"
        if result[0:3] == '1.0':
            result = result[3:]

        return result

    def add(self, n, sign):
        try:
            if float(n) == 0:
                return self.char
        except ValueError:
            pass
        divided = False
        try:
            factor = float(get_elements_until(self.char, 'x'))
        except ValueError:  # if an error is raised, then the compiler couldn't convert / to float then the element is divided
            factor = float(get_elements_until(self.char, 'x')[:-1])
            divided = True
        if 'x' in str(n):
            n_factor = float(get_elements_until(n, 'x'))

            if not divided:
                if sign:
                    result = f'{factor + n_factor}{self.char}'
                else:
                    result = f'{factor - n_factor}{self.char}'
            elif divided:
                if sign:
                    result = f'{factor + n_factor}/{self.char}'
                else:
                    result = f'{factor - n_factor}/{self.char}'

            return result
        else:
            if sign:
                result = f'{self.char} + {n}'
            else:
                result = f'{self.char} - {n}'
        return result


def is_calculable(func):
    from math_calcul2.helping_function import has_sublists
    from math_calcul2.calculating_function import calculate1


    def check(array):
        if not has_sublists(array) and (len(array) == 1 or len(array) >= 3):
            return func(array)
        else:
            if has_sublists(array):
                return func(calculate1(array))

    return check


def is_calculable2(func):
    from math_calcul2.helping_function import has_sublists

    def check(array):
        if not has_sublists(array):
            return func(array)
        else:
            return array

    return check


def redistribute(big_array):
    from math_calcul2.helping_function import has_sublists
    from math_calcul2.helping_function2 import find_indices, check_if_string_with_x
    from math_calcul2.calculating_function import calculate_normal_sub_array2

    if has_sublists(big_array):
        index_counter = -1
        for array in big_array:
            index_counter += 1
            if array.__class__ == list:
                if has_sublists(
                        array):  # If the array has sublist, then we have to use the distribution properties in math, if not we only have to calculate it
                    multi_division_indexes = find_indices(array, ('*', '/'))
                    for index in multi_division_indexes:
                        if array[index] == '*':
                            sign = True
                        else:
                            sign = False
                        if array[index - 1].__class__ == list:
                            sub_array = array[index - 1]
                            multiplier = array[index + 1]
                            result = []
                            skip_next = 0
                            for i in range(len(sub_array)):
                                if skip_next > 0:
                                    skip_next -= 1
                                    continue
                                try:
                                    result.append(float(sub_array[i]) * float(multiplier))
                                except ValueError or TypeError:
                                    result = math_distribution(sub_array[i], multiplier, sign, result)

                                try:
                                    result.append(sub_array[i + 1])
                                    skip_next += 1
                                except IndexError:
                                    pass
                            result = [item.char if isinstance(item, UnknownNumber) else item for item in result]
                            big_array = big_array[:index_counter] + result + big_array[index_counter + 1:]

                else:
                    big_array[index_counter] = calculate_normal_sub_array2(array)

    return simplify(
        big_array)  # after redistributing the bigarray , now we only have to gather unknown elements and known elements


def math_distribution(item, multiplier, sign, result=None):
    if result is None:
        result = []
    from math_calcul2.helping_function2 import check_if_string_with_x
    item1_is_unknown, item2_is_unknown = check_if_string_with_x(item, multiplier)
    if item1_is_unknown and not item2_is_unknown:
        unknown_number = UnknownNumber(char=item)
        calculation = UnknownNumber(unknown_number.multiply(float(multiplier), sign, before=False))
        result.append(calculation)
    elif item2_is_unknown and not item1_is_unknown:
        unknown_number = UnknownNumber(char=multiplier)
        calculation = UnknownNumber(unknown_number.multiply(float(item), sign, before=True))
        result.append(calculation)
    elif item1_is_unknown and item2_is_unknown:
        unknown_number1 = UnknownNumber(char=item)
        unknown_number2 = UnknownNumber(char=multiplier)
        calculation = UnknownNumber(unknown_number1.multiply(unknown_number2.char, sign))
        result.append(calculation)
    return result


def simplify(big_array):
    from math_calcul2.calculating_function import calculate_normal_sub_array, signs
    if len(big_array) == 0:
        return big_array[0]
    result = []
    unknown_values = dict()
    known_values = []
    skip_next = 0
    index_counter = -1
    for n in big_array:
        index_counter += 1
        if skip_next > 0:
            skip_next -= 1
            continue
        if index_counter > 0:
            add_sign = True
        else:
            add_sign = False
        if 'x' in str(n):
            x_index = n.index('x')
            # if x is in n, then n is an unknown number, and we must know if it raised to power, or divided, or divided and raised to a power, or just multiplied
            try:
                unknown_values = handle_power(n, x_index, unknown_values)
                unknown_values = handle_sign(n, x_index, unknown_values, signs)
                unknown_values = handle_division_power(n, x_index, unknown_values)
                unknown_values = handle_division(n, x_index, unknown_values)
                skip_next += 1
                # if an index error occurred, then either the index equal zero, or the index is less that the length by one
                continue
            except IndexError:
                if x_index > 0:  # if it is bigger than zero, than the other condition is false
                    if n[x_index - 1] == '/':
                        if add_sign:
                            unknown_values.setdefault(f"/x", []).append(big_array[index_counter - 1])

                        unknown_values.setdefault(f"/x", []).append(n)

                    else:
                        if add_sign:
                            unknown_values.setdefault('x', []).append(big_array[index_counter - 1])
                        unknown_values.setdefault('x', []).append(n)

                else:
                    if n[x_index + 1] == '^':
                        if add_sign:
                            unknown_values.setdefault(f"x^{n[x_index + 2]}", []).append(big_array[index_counter - 1])
                        unknown_values.setdefault(f"x^{n[x_index + 2]}", []).append(n)

                    else:
                        if add_sign:
                            unknown_values.setdefault('x', []).append(big_array[index_counter - 1])
                        unknown_values.setdefault('x', []).append(n)
            skip_next += 1
        else:

            if add_sign:
                known_values.append(big_array[index_counter - 1])

            known_values.append(n)
            skip_next += 1

    for key in unknown_values.keys():
        if len(key) > 1:
            limit = key[0]
        else:
            limit = key  # get the factor for each key stored in the dict, and then calculate their sum
        unknown_values[key] = [get_elements_until(item, limit) for item in unknown_values[key]]
        if unknown_values[key][0] == '+':
            unknown_values[key] = unknown_values[key][1:]
        unknown_values[key] = calculate_normal_sub_array(unknown_values[key])
        if unknown_values[key] == float(1):
            result.append('+')
            result.append(f'{key}')  # if the factor is equal to one, then no need to add it
        else:
            result.append('+')
            result.append(f'{unknown_values[key]}{key}')

    for value in known_values:
        result.append(value)

    if result[0] == '+':
        result = result[1:]
    return result


def handle_power(n, x_index, unknown_values):
    if n[x_index + 1] == '^' and n[x_index - 1] != '/':
        unknown_values.setdefault(f"x^{n[x_index + 2]}", []).append(n)
    return unknown_values


def handle_sign(n, x_index, unknown_values, signs):
    if n[x_index - 1] != '/' and n[x_index + 1] in signs:
        unknown_values.setdefault('x', []).append(n)
    return unknown_values


def handle_division_power(n, x_index, unknown_values):
    if n[x_index - 1] == '/' and n[x_index + 1] == '^':
        unknown_values.setdefault(f"/x^{n[x_index + 2]}", []).append(n)
    return unknown_values


def handle_division(n, x_index, unknown_values):
    if n[x_index - 1] == '/' and n[x_index + 1] != '^':
        unknown_values.setdefault(f"/x", []).append(n)
    return unknown_values
