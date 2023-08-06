from dataclasses import dataclass
from typing import Union


@dataclass
class Calculator():
    """ Basic calculator which performs some basic arithmetic operations
        operations including: (+, -, *, /, nth root)

    Returns:
        memory of calculator after operation
    """
    memory: float = 0.0  # Define the memory attribute and initialize it to 0.0

    def valid_operation_check(self, number, operation: str) -> bool:
        # check if the input number is a float or int and handle ZeroDivisionError
        try:
            if not isinstance(number, (float, int)):
                raise TypeError(
                    f"The input number should be a float or int, not {type(number)}. Returning the current memory:")
            if operation == 'division' and number == 0.0:
                raise ZeroDivisionError(
                    "Division by zero is not allowed. Returning the current memory:")
        except (TypeError, ZeroDivisionError) as e:
            print(e)
            return False
        return True

    def add(self, number: float) -> float:
        # add number on top of the calculator memory
        if self.valid_operation_check(number, 'addition'):
            self.memory += number
        return self.memory

    def subtract(self, number: float) -> float:
        # subtract number from the calculator memory
        if self.valid_operation_check(number, 'subtraction'):
            self.memory -= number
        return self.memory

    def multiply(self, number: float) -> float:
        # multiply the calculator memory by the number
        if self.valid_operation_check(number, 'multiplication'):
            self.memory *= number
        return self.memory

    def divide(self, number: float) -> float:
        # divide the calculator memory by the number
        if self.valid_operation_check(number, 'division'):
            self.memory /= number
        return self.memory

    def root(self, n: Union[int, float]) -> float:
        # compute the nth root of the calculator memory
        if n <= 0:
            print('The value of n should be greater than 0.')
        else:
            self.memory = self.memory ** (1.0/n)
        return self.memory

    def reset(self) -> float:
        # resets the memory to 0.0
        self.memory = 0.0
        return self.memory
