"""A simple Calculator with memory. Can perform addition, subtraction,
multiplication, division and extraction of nth root. Memory can be reset to 0.
Meant to be used with int numbers. First the user has to instantiate
a Calculator object. Starting memory can be specified but the default is 0.
Then one of the previously mentioned methods can be used.

Example:
    calc = Calculator()
    calc.add(5)
    > 5
    calc.subtract(1)
    > 4
    calc.multiply_by(8)
    > 32
    calc.divide_by(2)
    > 16.0
    calc.root_extraction(4)
    > 2.0
    """


class Calculator:
    """A simple Calculator with memory. Can perform addition, subtraction,
    multiplication, division and extraction of nth root. Memory can be reset to 0.
    Starting memory can be specified but the default is 0."""

    def __init__(self, memory: int = 0):
        self.memory = memory

    def __str__(self):
        return f"Current memory is {self.memory}"

    def add(self, number: int) -> int:
        """Simple addition function. Adds a specified number to calculators' memory"""
        self.memory = self.memory + number
        return self.memory

    def subtract(self, number: int) -> int:
        """Simple subtraction function. Subtracts a specified number from calculators' memory"""
        self.memory = self.memory - number
        return self.memory

    def multiply_by(self, number: int) -> int:
        """Simple multiplication function. Multiplies calculators' memory by a specified number"""
        self.memory = self.memory * number
        return self.memory

    def divide_by(self, number: int) -> float:
        """Simple division function. Divides calculators' memory by a specified number.
        If the user tries to divide by zero, ZeroDivisionError will be raised."""
        try:
            self.memory = self.memory / number
            return self.memory
        except ZeroDivisionError:
            print('Cannot divide by 0')
            return self.memory

    def root_extraction(self, number: int) -> float:
        """Root extraction function. Extracts specified root from number
        in calculators' memory.

        Example of extracting a -3 root from calculators memory:
        calc = Calculator(-8)
        > New calculator object created. Current total is -8
        calc.root_extraction(3)
        > -2.0

        If the user specifies too big
        or too small of a number OverflowError will be raised. If the user
        specifies 0 as the number, ZeroDivisionError will be raised.
        Does not allow the user to extract an even root from a negative number."""
        try:
            if number % 2 == 0 and self.memory < 0:
                print('Cannot take an even root out of a negative number')
                return self.memory
            else:
                self.memory = self.memory ** (1 / number)
                return self.memory
        except ZeroDivisionError:
            print('Cannot divide by 0')
            return self.memory
        except OverflowError:
            print('Extracting the root with a specified number results in '
                  'a number that is too large')
            return self.memory

    def reset(self):
        """A function to reset the calculators' memory to 0"""
        self.memory = 0
