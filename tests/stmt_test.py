import unittest
from Parser import *
from Scanner import *
from ASTVisitor import *

test_asts = {
    'a = 1;': AssignAST(IdAST('a'), IntegerAST(1)),
    'b = 1;': AssignAST(IdAST('b'), IntegerAST(1)),
    'a > b': BinaryOPAST('>', IdAST('a'), IdAST('b')),
    'begin end': CompoundStmtASt(),
}


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
        src = 'begin end'
        self.cmp_ast(src, test_asts[src])

    def test_cmp_lt(self):
        scanner = Scanner('a > b')
        scanner.lex()

        parser = Parser(scanner.tokens)
        ast = parser.expr()
        self.assertEqual(ast, test_asts['a > b'])

    def test_assign(self):
        code = '''
        begin
            a = 1;
        end
        '''
        self.cmp_ast(code, CompoundStmtASt(AssignAST(IdAST('a'), IntegerAST(1))))

    def test_assign_2(self):
        code = '''
        begin
           a = 1;
           b = 2;
        end
                '''
        self.cmp_ast(code, CompoundStmtASt(AssignAST(IdAST('a'), IntegerAST(1)),
                                           AssignAST(IdAST('b'), IntegerAST(2))))

    def test_if_stmt_1(self):
        code = '''
        begin
            if a > b then
            begin
                a = 1;
            end
        end
        '''
        self.cmp_ast(code, CompoundStmtASt(
            IfAST(
                test_asts['a > b'],
                CompoundStmtASt(
                    test_asts['a = 1;']
                ),
                None
            )
        ))

    def test_if_stmt_2(self):
        code = '''
        begin
            if a > b then
            begin
                a = 1;
            end
            else
            begin
                b = 1;
            end
        end
        '''
        self.cmp_ast(code, CompoundStmtASt(
            IfAST(
                test_asts['a > b'],
                CompoundStmtASt(
                    test_asts['a = 1;']
                ),
                CompoundStmtASt(
                    test_asts['b = 1;']
                )
            )
        ))

    def test_while_stmt_1(self):
        code = '''
        begin
            while a > b do
            begin
                a = 1;
                b = 1;
            end
        end
        '''
        self.cmp_ast(code, CompoundStmtASt(
            WhileAST(
                test_asts['a > b'],
                CompoundStmtASt(
                    test_asts['a = 1;'],
                    test_asts['b = 1;']
                )
            )
        ))

    def test_for_stmt_1(self):
        code = '''
        begin
            for a in as do
            begin
                a = 1;
                b = 1;
            end
        end
        '''
        self.cmp_ast(code, CompoundStmtASt(
            ForAST(
                IdAST('a'),
                IdAST('as'),
                CompoundStmtASt(
                    test_asts['a = 1;'],
                    test_asts['b = 1;']
                )
            )
        ))

    def test_if_eval_1(self):
        """
        a = 3;
        b = 4;
        if (a > b) then
            a = 1;
        else
            b =1;
        :return:
        """
        if_stmt = CompoundStmtASt(
            AssignAST(IdAST('a'), IntegerAST(3)),
            AssignAST(IdAST('b'), IntegerAST(4)),
            IfAST(
                test_asts['a > b'],
                CompoundStmtASt(
                    test_asts['a = 1;']
                ),
                CompoundStmtASt(
                    test_asts['b = 1;']
                )
            )
        )

        eval_visitor = ASTEvalVisitor()
        res = eval_visitor.eval(if_stmt)
        print(res)

    def x_test_func_decl_1(self):
        code = """
        def cmp(a, b) begin
            a = 3;
            b = 4;
            if (a > b) then
                a = 1;
            else
                b =1;
        end
        """
        self.cmp_ast(code, FunctionAST(
            IdAST('cmp'),
            [IdAST('a'), IdAST('b')],
            CompoundStmtASt(
                AssignAST(IdAST('a'), IntegerAST(3)),
                AssignAST(IdAST('b'), IntegerAST(4)),
                IfAST(
                    test_asts['a > b'],
                    CompoundStmtASt(
                        test_asts['a = 1;']
                    ),
                    CompoundStmtASt(
                        test_asts['b = 1;']
                    )
                )
            )
        ))

    def test_func_decl_2(self):
        code = """
            def empty() begin end
        """
        self.cmp_ast(code, FunctionAST(
            IdAST('empty'), [], CompoundStmtASt(), None
        ))
