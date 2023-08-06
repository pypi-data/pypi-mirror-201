class Calculator:
    """
    This class represents calculator that can perform simple arithmetic operations. Calculator has a memory.
    """
    def __init__(self):
        """
        Sets initial calculator's memory to 0.
        """
        self.memory = 0.0

    def add(self, value: float) -> float:
        """
        Adds argument to the value saved in memory.

        :param value: Float/ int value to be added to the memory value.
        :return: memory value after addition.
        """
        self.memory += value
        return self.memory

    def substract(self, value: float) -> float:
        """
        Substracts argument from the value saved in memory.
        :param value: Float/ int value to be substracted from the memory value.
        :return: memory value after substraction.
        """
        self.memory -= value
        return self.memory

    def multiply(self, value: float) -> float:
        """
        Multiplies value saved in memory by the provided value.
        :param value: Float/ int value by which to multiply the in-memory value.
        :return: memory value after multiplication.
        """
        self.memory = self.memory * value
        return self.memory

    def divide(self, value: float) -> float:
        """
        Divides value saved in memory by the provided value.
        :param value: Float/ int value by which to divide the in-memory value.
        :return: memory value after division.
        """
        self.memory = self.memory / value
        return self.memory

    def root(self, n: int) -> float:
        """
        Raise the value saves in memory to the power of 1 divided by the provided value.
        :param n: Float/ int value used as 1/ n.
        :return: memory value after root.
        """
        self.memory = self.memory ** (1/n)
        return self.memory

    def reset(self) -> float:
        """
        Resseting value in memory to zero.
        :return:
        """
        self.memory = 0
        return self.memory
