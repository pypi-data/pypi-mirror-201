import unittest

from file.calculator import Calculator


class TestCalculator(unittest.TestCase):

    def setUp(self) -> None:
        self.calculator = Calculator()

    def test_add(self):
        self.assertEqual(self.calculator.memory, 0)
        self.assertEqual(self.calculator.add(5), 5)
        self.assertEqual(self.calculator.add(5), 10)
        self.assertEqual(self.calculator.add(6), 16)
        self.assertEqual(self.calculator.memory, 16)
        self.assertEqual(self.calculator.reset(), 0)

    def test_substract(self):
        self.assertEqual(self.calculator.memory, 0)
        self.assertEqual(self.calculator.substract(5), -5)
        self.assertEqual(self.calculator.substract(3), -8)
        self.assertEqual(self.calculator.memory, -8)
        self.assertEqual(self.calculator.reset(), 0)

    def test_multiply(self):
        self.assertEqual(self.calculator.memory, 0)
        self.assertEqual(self.calculator.add(2), 2)
        self.assertEqual(self.calculator.multiply(4), 8)
        self.assertEqual(self.calculator.memory, 8)
        self.assertEqual(self.calculator.reset(), 0)

    def test_divide(self):
        self.assertEqual(self.calculator.memory, 0)
        self.assertEqual(self.calculator.add(4), 4)
        self.assertEqual(self.calculator.divide(2), 2)
        self.assertEqual(self.calculator.memory, 2)
        self.assertEqual(self.calculator.reset(), 0)

    def test_root(self):
        self.assertEqual(self.calculator.memory, 0)
        self.assertEqual(self.calculator.root(2), 0)
        self.assertEqual(self.calculator.add(4), 4)
        self.assertEqual(self.calculator.root(2), 2)
        self.assertEqual(self.calculator.memory, 2)
        self.assertEqual(self.calculator.reset(), 0)