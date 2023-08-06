# BruzaiteCalculator Package
This package provides a simple calculator with memory that can perform basic arithmetic operations. The BruzaiteCalculator class supports addition, subtraction, multiplication, division, taking the nth root of a number, and resetting the calculator's memory.


# Table of Contents
Requirements
Recommended modules
Installation
Configuration
Troubleshooting
Limitations
FAQ
Maintainers

# Requirements
The main package file should contain a class BruzaiteCalculator that should be able to perform these actions:

Addition / Subtraction.
Multiplication / Division.
Take (n) root of a number.
Reset memory (Calculator must have its own memory, meaning it should manipulate its starting number 0 until it is reset.).
This means that, for example, calculator should perform actions with a value inside its memory (for this example, the value inside the calculator's memory is 0): calculator.add(2) results in 2.

# Recommended modules
Python 3.x

# Installation
To install the BruzaiteCalculator package, run the following command:

Copy code
pip install BruzaiteCalculator

# Configuration
There is no configuration required for this package.

# Troubleshooting
If you encounter any issues while using the BruzaiteCalculator package, please refer to the package documentation or contact the maintainers for support.

# Limitations
You must create an instance of the BruzaiteCalculator class to use its methods.
The methods only work with integers and floats. If you provide any other data types, a TypeError exception will be raised.
If you try to divide by zero (Calculator.divide(0)), a ZeroDivisionError exception will be raised.
If the result of the nth_root() method is too large to be represented, an OverflowError exception will be raised.
If you provide more arguments than needed, a ValueError exception will be raised.

# FAQ
Q: How do I add two numbers?

A: You can add two numbers using the add() method of the BruzaiteCalculator class. For example:

from BruzaiteCalculator import BruzaiteCalculator

calculator = BruzaiteCalculator()
calculator.add(2)
calculator.add(3)
print(calculator.memory) # Output: 5


Q: How do I subtract two numbers?

A: You can subtract two numbers using the subtract() method of the BruzaiteCalculator class. For example:

from BruzaiteCalculator import BruzaiteCalculator

calculator = BruzaiteCalculator()
calculator.subtract(3)
calculator.subtract(2)
print(calculator.memory) # Output: -5

Q: How do I multiply two numbers?

A: You can multiply two numbers using the multiply() method of the BruzaiteCalculator class. For example:

from BruzaiteCalculator import BruzaiteCalculator

calculator = BruzaiteCalculator()
calculator.multiply(2)
calculator.multiply(3)
print(calculator.memory) # Output: 6

Q: How do I divide two numbers?

A: You can divide two numbers using the divide() method of the BruzaiteCalculator class. For example:

from BruzaiteCalculator import BruzaiteCalculator

calculator = BruzaiteCalculator()
calculator.divide(6)
calculator.divide(2)
print(calculator.memory) # Output: 1.5

Q: How do I take the nth root of a number?

A: You can take the nth root of a number using the nth_root() method of the BruzaiteCalculator class. For example:

from calculator import BruzaiteCalculator

calculator = BruzaiteCalculator()
calculator.add(8)
calculator.nth_root(3)
print(calculator.memory) # Output: 2.0

Q: How do I reset the calculator's memory?
A: You can reset the calculator's memory to 0 using the reset() method of the BruzaiteCalculator class. For example:

from calculator import BruzaiteCalculator

calculator = BruzaiteCalculator()
calculator.add(2)
calculator.reset()
print(calculator.memory) # Output: 0

# Maintainers
This package is maintained by Ausra Bruzaite. If you have any questions or issues, please contact bruzaite.ausra@gmail.com.




