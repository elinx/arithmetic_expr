import unittest
from Parser import *
from Scanner import *
from ASTVisitor import *


class ArithmeticTest(unittest.TestCase):

    def common(self, expr, expect):
        scanner = Scanner(expr)
        scanner.lex()

        parser = Parser(scanner.tokens)
        ast = parser.parse()

        eval_visitor = ASTEvalVisitor()
        res = eval_visitor.eval(ast)

        disp_visitor = ASTDisplayVisitor()
        disp_visitor.display(ast)

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

    def test_unary(self):
        self.common('2 + -3', -1)

    def test_parenthsis(self):
        self.common('(2 + 3) * 6', 30)
