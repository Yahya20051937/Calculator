from unittest import TestCase
from math_calcul.math_functions import sort_calcul_list, sub_calcul2, get_indexes, func_calcul
from functions.my_functions import replace_sequence_in_array, divider_into_multiplier, gather_elements
from math_calcul.equations import solve_degree_two_equations
from math_calcul2.organizing_function import organize_calcul_list


class Test(TestCase):
    def test_sub_calcul2(self):
        self.assertEqual(sub_calcul2([2, '+', 3]), 5)
        self.assertEqual(sub_calcul2([4, '-', 2]), 2)
        self.assertEqual(sub_calcul2([3, '-', 4, '+', 2]), 1)
        self.assertEqual(sub_calcul2([5, '+', 2, '-', 1, '-', 3]), 3)

    def test_sort_calcul(self):
        self.assertEqual(sort_calcul_list(['(', 2, '+', 3, ')', '+', 4]), [[5], '+', [4]])
        self.assertEqual(sort_calcul_list([5, '-', '(', 2, '+', 3, ')']), [[5], '-', [5]])
        self.assertEqual(sort_calcul_list([1, '+', 2, '-', 3, '+', 4, '-', 5]),
                         [[1], '+', [2], '-', [3], '+', [4], '-', [5]])
        self.assertEqual(sort_calcul_list([1, '+', '(', 2, '-', 3, '+', 4, '-', 5, ')']),
                         [[1], '+', [-2]])
        self.assertEqual(sort_calcul_list(['(', 2, '*', 3, ')', '+', 4]), [[2, '*', 3], '+', [4]])

    def test_get_indexes(self):
        # Test case 1
        array_1 = [1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1]
        key_1 = 5
        expected_output_1 = [4, 6]
        self.assertEqual(get_indexes(array_1, key_1), expected_output_1)

        # Test case 2
        array_2 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        key_2 = 'g'
        expected_output_2 = [6]
        self.assertEqual(get_indexes(array_2, key_2), expected_output_2)

        # Test case 3
        array_3 = ['apple', 'banana', 'cherry', 'apple', 'date', 'elderberry']
        key_3 = 'pear'
        expected_output_3 = []
        self.assertEqual(get_indexes(array_3, key_3), expected_output_3)

    def test_ln(self):
        self.assertAlmostEqual(func_calcul('ln', [16649]), 9.72, delta=0.1)
        self.assertAlmostEqual(func_calcul('ln', [92]), 4.52, delta=0.1)
        self.assertIsNone(func_calcul('ln', [0]))
        self.assertIsNone(func_calcul('ln', [-1]))

    def test_exp(self):
        self.assertAlmostEqual(func_calcul('exp', [5]), 148.413, delta=0.1)
        self.assertAlmostEqual(func_calcul('exp', [0]), 1, delta=0.1)

    def test_replace_sequence(self):
        sequences = ["ln", "exp"]
        array = ["l", "n", "(", "x", ")", "e", "x", "p"]
        expected_output = ["ln", "(", "x", ")", "exp"]
        output = replace_sequence_in_array(sequences, array)
        self.assertEqual(output, expected_output)

    def test_replace_sequence_with_multiple_occurrences(self):
        sequences = ["ln", "exp"]
        array = ["l", "n", "(", "x", ")", "e", "x", "p", "l", "n", "(", "y", ")", "e", "x", "p"]
        expected_output = ["ln", "(", "x", ")", "exp", "ln", "(", "y", ")", "exp"]
        output = replace_sequence_in_array(sequences, array)
        self.assertEqual(output, expected_output)

    def test_divider_into_multiplier_basic(self):
        factors = [2, '/', 4]
        expected_result = [2, '*', 0.25]
        self.assertEqual(divider_into_multiplier(factors), expected_result)

    def test_divider_into_multiplier_multiple_divisions(self):
        factors = [4, '/', 2, '/', 5]
        expected_result = [4, '*', 0.5, '*', 0.2]
        self.assertEqual(divider_into_multiplier(factors), expected_result)

    def test_discriminant_zero(self):
        result = solve_degree_two_equations("2x^2 + 8x + 8 = 0")
        self.assertAlmostEqual(result, -2.0)

    def test_discriminant_positive(self):
        result1, result2 = solve_degree_two_equations("x^2 - 3x - 10 = 0")
        self.assertTrue(result1 in [5.0, -2.0])
        self.assertTrue(result2 in [5.0, -2.0])

    def test_discriminant_negative(self):
        result = solve_degree_two_equations("x^2 + 2x + 5 = 0")
        self.assertEqual(result, None)

    def test_modify_array_with_cos(self):
        arr = ['cos', '(', 6, 'x', ')', '+', 12]
        expected = ['cos(6x)', '+', 12]
        actual = gather_elements('cos', arr)
        self.assertEqual(actual, expected)

    def test_modify_array_with_sin(self):
        arr = ['sin', '(', 6, 'x', ')', '+', 12]
        expected = ['sin(6x)', '+', 12]
        actual = gather_elements('sin', arr)
        self.assertEqual(actual, expected)

    def test_modify_array_with_ln(self):
        arr = ['ln', '(', 6, 'x', ')', '+', 12]
        expected = ['ln(6x)', '+', 12]
        actual = gather_elements('ln', arr)
        self.assertEqual(actual, expected)

    def test_modify_array_with_exp(self):
        arr = ['exp', '(', 6, 'x', ')', '+', 12]
        expected = ['exp(6x)', '+', 12]
        actual = gather_elements('exp', arr)
        self.assertEqual(actual, expected)

    def test_modify_array_without_functions(self):
        arr = ['x', '+', 12]
        expected = arr
        actual = gather_elements('cos', arr)
        self.assertEqual(actual, expected)

    def test_modify_array_with_duplicated_exp(self):
        arr = ['exp', '(', 2, 'x', ')', '-', 'exp', '(', 2, 'x', ')', '+', 7]
        expected = ['exp(2x)', '-', 'exp(2x)', '+', 7]
        actual = gather_elements('exp', arr)
        self.assertEqual(actual, expected)

    def test_expression1(self):
        expression = ['[', '(', '5', '+', '3', ')', '/', '2', '-', '8', '*', '4', '+', '5', '*', 'ln', '(', '2', ')',
                      ']', '/', '[', '(', '4', '+', 'exp', '(', '10', ')', ')', '*', '10', '-', 'ln', '(', '{', '2',
                      '*', '5', '}', '-', '1', ')', ']']
        expected_result = -0.00011136627351609195
        result = organize_calcul_list(expression)
        self.assertAlmostEqual(result, expected_result)

    def test_expression2(self):
        expression = ['[', '(', '7', '-', '2', ')', '*', '(', '3', '+', '4', ')', '-', 'exp', '(', '2', ')', '+', 'ln',
                      '(', '5', ')', ']', '/', '[', 'sqrt', '(', '16', ')', '+', '2', '*', '(', '6', '-', '3', ')', ']']
        expected_result = 2.9220381813503447
        result = organize_calcul_list(expression)
        self.assertAlmostEqual(result, expected_result)

    def test_expression3(self):
        expression = ['[', 'sin', '(', '30', ')', '+', 'ln', '(', '100', ')', ']', '/', '[', 'sqrt', '(', '25', ')',
                      '-', 'cos', '(', '45', ')', ']']
        expected_result = 1.1892143423495523
        result = organize_calcul_list(expression)
        self.assertAlmostEqual(result, expected_result)

    def test_expression4(self):
        expression = ['(', '3', '*', '4', ')', '+', '(', '8', '/', '2', ')', '-', '(', 'sqrt', '(', '9', ')', '*', '2',
                      ')']
        expected_result = 10
        result = organize_calcul_list(expression)
        self.assertAlmostEqual(result, expected_result)

    def test_expression5(self):
        expression = ['[', '(', '5', '+', '2', ')', '*', '(', '3', '-', '1', ')', ']', '/', '[', '(', '4', '+', '1',
                      ')', ']']
        expected_result = 2.8
        result = organize_calcul_list(expression)
        self.assertAlmostEqual(result, expected_result)

    def test_expression6(self):
        expression = ['[', '(', '6', '+', '2', ')', '*', '(', '9', '-', '3', ')', '+', '4', ']', '/', '[', '(', '5',
                      '+', '1', ')', '*', '(', '3', '-', '2', ')', ']']
        expected_result = 8.66666666666666666666666666
        result = organize_calcul_list(expression)
        self.assertAlmostEqual(result, expected_result)

