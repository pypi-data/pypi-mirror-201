import unittest
from bruzaite_calculator import BruzaiteCalculator
import sys
import os

# add the parent directory of the current file to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestCalculator(unittest.TestCase):
    def test_add_method_adds_correctly_to_memory(self):
        calculator = BruzaiteCalculator()
        result = calculator.add(5)
        self.assertEqual(result, 5)
        result = calculator.add(7.5)
        self.assertEqual(result, 12.5)
        result = calculator.add('abc')
        self.assertEqual(result, 12.5)
        result = calculator.add(None)
        self.assertEqual(result, 12.5)

    def test_subtract_method_subtracts_correctly_from_memory(self):
        calculator = BruzaiteCalculator()
        result = calculator.subtract(5)
        self.assertEqual(result, -5)
        result = calculator.subtract(7.5)
        self.assertEqual(result, -12.5)
        result = calculator.subtract('abc')
        self.assertEqual(result, -12.5)
        result = calculator.subtract(None)
        self.assertEqual(result, -12.5)

    def test_multiply_method_multiplies_correctly_to_memory(self):
        calculator = BruzaiteCalculator()
        result = calculator.multiply(5)
        self.assertEqual(result, 0)
        result = calculator.multiply(3.5)
        self.assertEqual(result, 0)
        result = calculator.multiply('abc')
        self.assertEqual(result, 0)
        result = calculator.multiply(None)
        self.assertEqual(result, 0)

    def test_divide_method_divides_correctly_to_memory(self):
        calculator = BruzaiteCalculator()
        calculator.add(10)
        result = calculator.divide(2)
        self.assertEqual(result, 5)
        result = calculator.divide('abc')
        self.assertEqual(result, 5)
        result = calculator.divide(None)
        self.assertEqual(result, 5)
        result = calculator.divide(0)
        self.assertEqual(result, 5)

    def test_nth_root_positive_integer(self):
        calculator = BruzaiteCalculator()
        calculator.memory = 27
        result = calculator.nth_root(3)
        self.assertEqual(result, 3)

    def test_nth_root_negative_integer_even_root(self):
        calculator = BruzaiteCalculator()
        calculator.memory = -8
        self.assertRaises(ValueError, calculator.nth_root, 4)

    def test_nth_root_negative_integer_odd_root(self):
        calculator = BruzaiteCalculator()
        calculator.memory = -27
        result = calculator.nth_root(3)
        self.assertEqual(result, -3)

    def test_nth_root_non_number(self):
        calculator = BruzaiteCalculator()
        self.assertRaises(TypeError, calculator.nth_root, 'abc')

    def test_reset_method_sets_memory_to_zero(self):
        calculator = BruzaiteCalculator()
        calculator.add(5)
        result = calculator.reset()
        self.assertEqual(result, 0)

    def test_init_method_initializes_memory_to_zero(self):
        calculator = BruzaiteCalculator()
        calculator.add(5)
        calculator.reset()
        self.assertEqual(calculator.memory, 0)

if __name__ == '__main__':
    unittest.main()
