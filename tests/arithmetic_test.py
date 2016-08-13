import unittest
from Parser import *
from Scanner import *


class ArithmeticTest(unittest.TestCase):

    def common(self, expr, expect):
        scanner = Scanner(expr)
        scanner.lex()

        parser = Parser(scanner.tokens)
        res = parser.exec(parser.parse())
        self.assertEqual(res, expect)

    def test_add(self):
        self.common('1 + 2', 3)

    def test_minus(self):
        self.common('5 - 3', 2)

    def test_mul(self):
        self.common('2 * 3', 6)

    def test_div(self):
        self.common('6 / 2', 3)

    def test_compound(self):
        self.common('2 + 3 * 6', 20)
