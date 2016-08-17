import unittest
from Parser import *
from Scanner import *
from ASTVisitor import *


class StmtTest(unittest.TestCase):

    def cmp_eval(self):
        pass

    def cmp_ast(self, expr, expect):
        scanner = Scanner(expr)
        scanner.lex()

        parser = Parser(scanner.tokens)
        ast = parser.parse()

        # eval_visitor = ASTEvalVisitor()
        # res = eval_visitor.eval(ast)

        # disp_visitor = ASTDisplayVisitor()
        # disp_visitor.display(ast)

        self.assertEqual(ast, expect)

    def test_assign(self):
        self.cmp_ast('begin a = 1; end', CompoundStmtASt(AssignAST('a', IntegerAST(1))))
