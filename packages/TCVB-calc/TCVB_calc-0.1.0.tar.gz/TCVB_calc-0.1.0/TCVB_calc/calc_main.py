class Calculator:
    def __init__(self, result=0):
        """Initializing the object, default value set to 0 if a value is not provided"""
        self.result = result

    def add(self, x):
        """Perform addition on the class object"""
        self.result += x

    def divide(self, x):
        """Perform division on the class object"""
        try:
            self.result /= x
        except ZeroDivisionError:
            print("Division by 0 is against science, resetting value to 0")
            self.result = 0

    def reset(self):
        """Reset the result attribute of the object to 0"""
        self.result = 0

    def subtract(self, x):
        """Perform subtraction on the class object"""
        self.result -= x

    def n_root(self, n):
        """Perform n'th root operation on the class object"""
        try:
            self.result = self.result ** (1 / n)
        except ZeroDivisionError:
            print("Division by 0 is against science, resetting value to 0")
            self.result = 0

    def multiply(self, x):
        """Perform multiplication on the class object"""
        self.result *= x


if __name__ == "__main__":
    Calculator()
