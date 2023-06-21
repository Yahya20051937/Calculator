def solve_degree_one_equation(E):
    from functions.my_functions import set_function, divider_into_multiplier, minus_array, remove_empty_arrays
    from math_calcul.math_functions import sort_calcul_list, sub_calcul1
    from math_calcul.math_functions import get_indexes
    from math_calcul.math_functions2 import calculate
    from functions.equation_functions import move_to_side2_1, get_factors
    signs = {'+': '-', '-': '+'}
    E_array = E
    if E.__class__ != list:
        E_array = set_function(E)

    equal_sign = get_indexes(E_array, '=')[0]

    side1 = sort_calcul_list(E_array[:equal_sign])
    side2 = sort_calcul_list(E_array[equal_sign + 1:])
    if (side2[0] == 0 or side2[0] == [0]) and len(side2) != 1:
        side2 = side2[1:]
    side1 = minus_array(side1)
    side1, side2 = remove_empty_arrays(side1), remove_empty_arrays(side2)
    side1, side2 = move_to_side2_1(side1, side2, signs)
    try:
        if side2[0] == '+':
            side2 = side2[1:]
    except IndexError:
        pass
    all_factors = get_factors(side1)
    factor = calculate(all_factors)
    side2 = minus_array(side2)
    side2 = [side2] + ['/'] + [factor]

    side2 = minus_array(side2)

    a = calculate(side2[0])
    b = calculate([side2[2]])
    x = calculate([[a, '/', b]])

    return x


def solve_degree_two_equations(E, j=False):
    from functions.my_functions import set_function
    from functions.equation_functions2 import move_to_side1, define_abc, nul_delta_solution, pos_delta_solution
    from math_calcul.math_functions import sort_calcul_list, get_indexes
    from math_calcul.math_functions2 import calculate

    signs = {'+': '-', '-': '+'}
    E_array = E
    if j is False:
        E_array = set_function(E)

    equal_sign = get_indexes(E_array, '=')[0]

    side1 = sort_calcul_list(E_array[:equal_sign])
    side2 = sort_calcul_list(E_array[equal_sign + 1:])

    side1, side2 = move_to_side1(side1, side2, signs)

    a, b, c = define_abc(side1)

    a, b = calculate(a), calculate(b)

    delta = b ** 2 - 4 * a * c

    if delta == 0:
        return nul_delta_solution(a, b)
    elif delta > 0:
        return pos_delta_solution(a, b, delta)
    else:
        return None


def solve_function_equation(E):
    from functions.my_functions import set_function
    from math_calcul.math_functions import sort_calcul_list, get_indexes
    from functions.my_functions import gather_elements
    signs = {'+': '-', '-': '+'}
    functions = ('cos', 'sin', 'ln', 'exp')
    E_array = set_function(E)

    equal_sign = get_indexes(E_array, '=')[0]

    side1 = sort_calcul_list(E_array[:equal_sign])
    side2 = sort_calcul_list(E_array[equal_sign + 1:])

    for f in functions:
        if f in side1:
            side1 = gather_elements(f, side1)
            break
    for f in functions:
        if f in side2:
            side2 = gather_elements(f, side2)
            break


solve_function_equation('cos(2x + 9) = 5')
