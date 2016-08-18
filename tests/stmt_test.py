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

    def test_empty(self):
        src = '''
        begin
        ;
        end
        '''
        self.cmp_ast(src, CompoundStmtASt())

    def test_assign(self):
        code = '''
        begin
            a = 1;
        end
        '''
        self.cmp_ast(code, CompoundStmtASt(AssignAST('a', IntegerAST(1))))

    def test_assign_2(self):
        code = '''
        begin
           a = 1;
           b = 2;
        end
                '''
        self.cmp_ast(code, CompoundStmtASt(AssignAST('a', IntegerAST(1)),
                                           AssignAST('b', IntegerAST(2))))
