from Scanner import *
from AST import *


class Parser:
    """Grammar:

    expr          ::= term ((PLUS | MINUS) term)*

    term          ::= factor ((MUL | DIV) factor)*

    factor        ::= NUM
                  |   PLUS NUM
                  |   MINUS NUM
                  |   '(' expr ')'

    compound_stmt ::= BEGIN stmt_list END

    stmt_list     ::= stmt
                  |   stmt SEMICOLON stmt_list

    stmt          ::= compound_stmt
                  |   if_stmt
                  |   while_stmt
                  |   assign_stmt
                  |   empty

    assign_stmt   ::= ID ASSIGN expr

    if_stmt       ::= IF expr THEN compound_stmt
                  |   IF expr THEN compound_stmt ELSE compound_stmt

    while_stmt    ::= WHILE expr DO compound_stmt
    """

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
            return IntegerAST(int(self.consume().val))
        if token.tag == RESERVED:
            if token.val == '+' or token.val == '-':
                op = self.consume()
                opd = IntegerAST(int(self.consume().val))
                return UnaryOPAST(op.val, opd)
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
            new_ast = BinaryOPAST(op.val, term_ast, right)
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
            new_ast = BinaryOPAST(op.val, expr_ast, right)
            expr_ast = new_ast
            token = self.peek()

        return expr_ast

    def parse(self):
        return self.expr()

