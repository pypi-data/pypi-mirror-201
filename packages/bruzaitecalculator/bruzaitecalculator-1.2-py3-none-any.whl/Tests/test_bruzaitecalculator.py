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
    
    def test_nth_root_positive_float_power(self):
        calculator = BruzaiteCalculator()
        calculator.memory = 16
        result = calculator.nth_root(0.5)
        self.assertAlmostEqual(result, 256, places=8)

    def test_nth_root_positive_integer_power(self):
        calculator = BruzaiteCalculator()
        calculator.memory = 8
        result = calculator.nth_root(3)
        self.assertAlmostEqual(result, 2, places=8)

    def test_nth_root_large_number_positive_integer_power(self):
        calculator = BruzaiteCalculator()
        calculator.memory = 1000000
        result = calculator.nth_root(6)
        self.assertAlmostEqual(result, 10, places=8)

    def test_nth_root_small_float_number(self):
        calculator = BruzaiteCalculator()
        calculator.memory = 0.0001
        result = calculator.nth_root(2)
        self.assertAlmostEqual(result, 0.01, places=8)

    def test_nth_root_float_number_and_float_power(self):
        calculator = BruzaiteCalculator()
        calculator.memory = 64.0
        result = calculator.nth_root(1.5)
        self.assertAlmostEqual(result, 8.0, places=8)
        
    def test_nth_root_memory_not_a_number(self):
        calculator = BruzaiteCalculator()
        calculator.memory = "not_a_number"
        self.assertRaises(TypeError, calculator.nth_root, 2)    
    
    def test_memory_initialization_and_reset(self):
        calculator = BruzaiteCalculator()
        self.assertEqual(calculator.memory, 0)  # Check if memory is initialized to 0
        
        calculator.add(5)
        calculator.reset()
        self.assertEqual(calculator.memory, 0)  # Check if memory is reset to 0

if __name__ == '__main__':
    unittest.main()
