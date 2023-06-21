import math
from collections import deque


def move_to_side1(side1, side2, signs):
    index_counter = -1

    for array in side2:
        if index_counter > 0:
            sign = side2[index_counter - 1]
            side2 = side2[:index_counter - 1] + side2[index_counter + 1:]
        else:
            sign = '+'
            side2 = side2[index_counter + 1:]
        opposite_sign = signs[sign]
        side1 = side1 + [opposite_sign] + [array]
    return side1, side2


def find_factor(array, var):
    index_counter = -1
    for n in array:
        index_counter += 1
        if n == var:
            if index_counter + 1 == len(array):
                factor = array[:index_counter]
            elif index_counter == 0:
                factor = array[index_counter + 2:]
            else:
                factor = array[:index_counter] + array[index_counter + 2:]
            return factor


def define_a(side1):
    for array in side1:
        if array.__class__ == list:
            index_counter = -1
            for n in array:
                index_counter += 1
                if n == 'x' and array[index_counter + 1] == '^' and array[index_counter + 2] == 2:
                    array = array[:index_counter] + ['x^2'] + array[index_counter + 3:]
                    a = find_factor(array, 'x^2')
                    side1.popleft()
                    if len(a) == 0:
                        a = [1]

                    return a


def define_b(side1):
    index_counter2 = -1
    for array in side1:
        index_counter2 += 1
        if array.__class__ == list:
            for n in array:
                if n == 'x':
                    b = find_factor(array, 'x')
                    if side1[index_counter2 - 1] == '-':
                        b.append(-1)
                        b = [b]

                    side1.popleft()
                    side1.popleft()
                    return b
    return [0]


def define_abc(side1):
    from functions.equation_functions import get_factors
    from functions.my_functions import minus_array
    a = 0
    b = 0
    t = 0
    from math_calcul.math_functions2 import calculate
    side1 = minus_array(side1)
    side1 = deque(side1)
    a = define_a(side1)
    b = define_b(side1)
    side1 = list(side1)
    if side1[0] == '+':
        side1 = side1[1:]
    if side1[0] == '+' or side1[0] == '-':
        side1 = [0] + side1
    c = calculate(side1)
    if len(a) == 2:
        a = [n for n in a if n.__class__ == int]
    if len(b) == 2:
        b = [n for n in b if n.__class__ == int]

    return a, b, c


def nul_delta_solution(a, b):
    x = -b/(2 * a)
    return x


def pos_delta_solution(a, b, delta):
    root_delta = math.sqrt(delta)

    x1 = (-b-root_delta)/(2*a)
    x2 = (-b+root_delta)/(2*a)

    return x1, x2


def move_side1_side2(side1, side2, f, signs):
    len_f = len(f)
    index_counter1 = -1
    for number in side1:
        index_counter1 += 1
        if























