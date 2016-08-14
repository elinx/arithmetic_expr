import unittest
from Scanner import *


class ScannerTest(unittest.TestCase):

    def common(self, expr, expect):
        scanner = Scanner(expr)
        scanner.lex()

        self.assertEqual(scanner.tokens, expect)

    def test_add(self):
        self.common('1 + 2', [Token('1', INT), Token('+', RESERVED), Token('2', INT)])

    def test_minus(self):
        self.common('5 - 3', [Token('5', INT), Token('-', RESERVED), Token('3', INT)])

    def test_mul(self):
        self.common('2 * 3', [Token('2', INT), Token('*', RESERVED), Token('3', INT)])

    def test_div(self):
        self.common('6 / 2', [Token('6', INT), Token('/', RESERVED), Token('2', INT)])

    def test_compound(self):
        self.common('2 + 3 * 6', [Token('2', INT), Token('+', RESERVED), Token('3', INT),
                                  Token('*', RESERVED), Token('6', INT)])

    def test_unary(self):
        self.common('2 + -3', [Token('2', INT), Token('+', RESERVED), Token('-', RESERVED),
                               Token('3', INT)])

    def test_parenthsis(self):
        self.common('(2 + 3) * 6', [Token('(', RESERVED), Token('2', INT), Token('+', RESERVED), Token('3', INT),
                                    Token(')', RESERVED), Token('*', RESERVED), Token('6', INT)])

