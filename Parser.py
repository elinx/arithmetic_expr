from Scanner import *


class Parser:
    """Grammar:

    expr ::= term ((PLUS | MINUS) term)*
    term ::= factor ((MUL | DIV) factor)*
    factor ::= NUM
            | PLUS NUM
            | MINUS NUM
            | '(' expr ')'
    """
    class AST:
        def __init__(self, value, left, right):
            self.value = value
            self.left = left
            self.right = right

        def __repr__(self, level=0):
            ret = '\t' * level + str(self.value) + '\n'
            if self.left is not None:
                ret += self.left.__repr__(level + 1)
            if self.right is not None:
                ret += self.right.__repr__(level + 1)
            return ret

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.ast = None

    def consume(self):
        token = None
        if self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            self.pos += 1
        return token

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def factor(self):
        """factor ::= [0-9]*"""
        token = self.peek()
        if token.tag == INT:
            return self.AST(self.consume().val, None, None)
        if token.tag == RESERVED:
            if token.val == '+' or token.val == '-':
                op = self.consume()
                opd = self.consume()
                return self.AST(op.val + opd.val, None, None)
            elif token.val == '(':
                self.consume()
                expr = self.expr()
                rp = self.peek()
                if rp.val == ')':
                    self.consume()
                    return expr
                else:
                    raise ValueError('need a `)`')
        return None

    def term(self):
        """term ::= factor ((MUL | DIV) factor)*"""
        term_ast = self.factor()

        token = self.peek()
        while token is not None and token.tag == RESERVED and \
                (token.val == '*' or token.val == '/'):
            op = self.consume()
            right = self.factor()
            new_ast = self.AST(op.val, term_ast, right)
            term_ast = new_ast
            token = self.peek()

        return term_ast

    def expr(self):
        """expr ::= term ((PLUS | MINUS) term)*"""
        expr_ast = self.term()

        token = self.peek()
        while token is not None and token.tag == RESERVED and \
                (token.val == '+' or token.val == '-'):
            op = self.consume()
            right = self.term()
            new_ast = self.AST(op.val, expr_ast, right)
            expr_ast = new_ast
            token = self.peek()

        return expr_ast

    def parse(self):
        self.ast = self.expr()
        return self.ast

    def exec(self, ast):
        if ast is not None and str(ast.value) not in '+-*/':
            return ast.value
        left = self.exec(ast.left)
        left = 0 if left is None else int(left)
        right = self.exec(ast.right)
        right = 0 if right is None else int(right)

        return {
            '+': left + right,
            '-': left - right,
            '*': left * right,
            '/': left / right
        }[ast.value]
