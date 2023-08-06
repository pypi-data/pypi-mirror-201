"""Calculator class with basic calculator functions"""

__version__ = "0.0.1"


class Calculator:

    def __init__(self, memory: float = 0.0) -> None:
        if type(memory) is not float and type(memory) is not int:
            raise TypeError("Wrong input format")
        self.memory: float = memory

    def __str__(self):
        return f"{self.memory}"

    def add(self, value: float) -> float:
        """Addition: sums calculator memory with provided value."""
        self.memory += value
        return self.memory

    def minus(self, value: float) -> float:
        """Subtraction: calculator memory minus the input value."""
        self.memory = self.memory - value
        return self.memory

    def multiply(self, value: float) -> float:
        """Multiplication: multiplies calculator memory by the input value."""
        self.memory = self.memory * value
        return self.memory

    def divide(self, value: float) -> float:
        """Division: devides the calculator memory by the input value."""
        if value == 0:
            raise ZeroDivisionError("Can't divide by zero")
        else:
            self.memory = self.memory / value
            return self.memory

    def root(self, n: int = 2) -> float:
        """Root: takes n root from the calculator memory value."""
        if self.memory < 0:
            raise ValueError("Can't take root from a negative number")

        elif n == 0:
            raise ValueError("Can't take zero root of a number")

        elif self.memory == 0 and n < 0:
            ZeroDivisionError("Can't take negative root of zero")

        else:
            self.memory = self.memory**(1/n)
            return self.memory

    def reset(self):
        """Resets the memory to zero."""
        self.memory = 0
        return self.memory


if (__name__ == '__main__'):
    print('Executing as standalone script:')
    calc = Calculator(5)
    print(f"{calc} + 4 = {calc.add(4)}")
    print(f"Root of {calc} = {calc.root()}")
    print(f"{calc} times 5 = {calc.multiply(5)}")
    print(f"{calc} divide by 3 = {calc.divide(3)}")
    print(f"Reseting memory: {calc.reset()}")
