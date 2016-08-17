import unittest
from Scanner import *


class ScannerTest(unittest.TestCase):

    def common(self, expr, expect):
        scanner = Scanner(expr)
        scanner.lex()

        self.assertEqual(scanner.tokens, expect)

    def test_int_1(self):
        self.common('1', [Token('1', INT)])

    def test_int_2(self):
        self.common('12', [Token('12', INT)])

    def test_id_1(self):
        self.common('a', [Token('a', ID)])

    def test_id_2(self):
        self.common('ab', [Token('ab', ID)])

    def test_id_3(self):
        self.common('ab3', [Token('ab3', ID)])

    def test_id_error(self):
        """not an acceptable identifier"""
        with self.assertRaises(UnacceptableInput):
            self.common('3ab', [])

    def test_and_op(self):
        self.common('and', [Token('and', RESERVED)])

    def test_or_op(self):
        self.common('or', [Token('or', RESERVED)])

    def test_not_op(self):
        self.common('not', [Token('not', RESERVED)])

    def test_lgt_op(self):
        self.common('>', [Token('>', RESERVED)])

    def test_st_op(self):
        self.common('<', [Token('<', RESERVED)])

    def test_le_op(self):
        self.common('>=', [Token('>=', RESERVED)])

    def test_se_op(self):
        self.common('<=', [Token('<=', RESERVED)])

    def test_eq_op(self):
        self.common('==', [Token('==', RESERVED)])

    def test_add(self):
        self.common('1 + 2', [Token('1', INT), Token('+', RESERVED), Token('2', INT)])

    def test_minus(self):
        self.common('5 - 3', [Token('5', INT), Token('-', RESERVED), Token('3', INT)])

    def test_mul(self):
        self.common('2 * 3', [Token('2', INT), Token('*', RESERVED), Token('3', INT)])

    def test_div(self):
        self.common('6 / 2', [Token('6', INT), Token('/', RESERVED), Token('2', INT)])

    def test_mix(self):
        self.common('2 + 3 * 6', [Token('2', INT), Token('+', RESERVED), Token('3', INT),
                                  Token('*', RESERVED), Token('6', INT)])

    def test_unary(self):
        self.common('2 + -3', [Token('2', INT), Token('+', RESERVED), Token('-', RESERVED),
                               Token('3', INT)])

    def test_parenthsis(self):
        self.common('(2 + 3) * 6', [Token('(', RESERVED), Token('2', INT), Token('+', RESERVED), Token('3', INT),
                                    Token(')', RESERVED), Token('*', RESERVED), Token('6', INT)])

    def test_gt_1(self):
        self.common('a > b', [Token('a', ID), Token('>', RESERVED), Token('b', ID)])

    def test_gt_2(self):
        self.common('1 > 2', [Token('1', INT), Token('>', RESERVED), Token('2', INT)])

    def test_if_stmt(self):
        self.common('if a > b then a else b', [
            Token('if', RESERVED), Token('a', ID),
            Token('>', RESERVED), Token('b', ID),
            Token('then', RESERVED), Token('a', ID),
            Token('else', RESERVED), Token('b', ID)
        ])

    def test_while_stmt(self):
        self.common('while a > b do a', [
            Token('while', RESERVED), Token('a', ID),
            Token('>', RESERVED), Token('b', ID),
            Token('do', RESERVED), Token('a', ID)
        ])

    def test_assign_1(self):
        self.common('a = 1', [Token('a', ID), Token('=', RESERVED), Token('1', INT)])

    def test_assign_2(self):
        self.common('a = b', [Token('a', ID), Token('=', RESERVED), Token('b', ID)])
