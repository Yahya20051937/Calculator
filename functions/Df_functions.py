def polynomial_different_from_zero_df(denominator, Df_set):
    from math_calcul.equations import solve_degree_two_equations, solve_degree_one_equation
    from functions.Df_function2 import check_first_second_degree
    base = denominator
    if 'x' in base:
        condition1, condition2, a = check_first_second_degree(base)

        if condition1 and condition2:
            side1 = ''
            for string in base[1:-1]:
                side1 += str(string)

            boundary_markers = solve_degree_two_equations(f'{side1} = 0')
            if boundary_markers.__class__ == tuple:
                Df_set.discard(boundary_markers[0])
                Df_set.discard(boundary_markers[1])
            elif boundary_markers.__class__ == int or boundary_markers.__class__ == float:
                Df_set.discard(boundary_markers)
            else:
                pass
        elif condition1:
            side1 = ''
            for string in base[1:-1]:
                side1 += str(string)

            boundary_marker = solve_degree_one_equation(f'{side1} = 0')

            Df_set.discard(boundary_marker)
    return Df_set


def ln_df(function_array, index_counter, Df_set):
    from math_calcul.equations import solve_degree_two_equations, solve_degree_one_equation
    from functions.Df_function2 import check_first_second_degree
    index_counter2 = index_counter
    for n in function_array[index_counter2:]:
        index_counter2 += 1
        if n == ')':
            inside_function = function_array[index_counter + 1:index_counter2]
            if 'x' in inside_function:
                condition1, condition2, a = check_first_second_degree(inside_function)

                if condition1 and condition2:
                    side1 = ''
                    for string in inside_function[1:-1]:
                        side1 += str(string)
                    boundary_markers = solve_degree_two_equations(f'{side1} = 0')
                    if boundary_markers is not None:
                        boundary_markers = sorted(boundary_markers)
                        if a > 0:
                            for number in range(boundary_markers[0], boundary_markers[1] + 1):
                                Df_set.discard(number)
                        elif a < 0:
                            for number in range(-1000, boundary_markers[0]):
                                Df_set.discard(number)
                            for number in range(boundary_markers[1], 1000 + 1):
                                Df_set.discard(number)
                    else:
                        return Df_set
                elif condition1:
                    side1 = ''
                    for string in inside_function[1:-1]:
                        side1 += str(string)
                    boundary_marker = solve_degree_one_equation(f'{side1} = 0')

                    if boundary_marker is not None:

                        if a > 0:

                            if boundary_marker.__class__ == int:
                                for number in range(-1000, boundary_marker + 1):
                                    Df_set.discard(number)
                            else:
                                for number in range(-1000, round(boundary_marker - 1) + 1):
                                    Df_set.discard(number)
                                Df_set.discard(boundary_marker)
                        elif a < 0:
                            if boundary_marker.__class__ == int:
                                for number in range(boundary_marker, 1000 + 1):
                                    Df_set.discard(number)
                            else:
                                for number in range(1000, round(boundary_marker + 1)):
                                    Df_set.discard(number)
                                Df_set.discard(boundary_marker)
                    else:
                        return Df_set

                return Df_set


def denominator_df(denominator, Df_set):
    if 'ln' not in denominator:
        Df_set = polynomial_different_from_zero_df(denominator, Df_set)

    return Df_set
