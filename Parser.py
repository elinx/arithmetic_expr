from Scanner import *
from AST import *


class Parser:
    """Grammar:

    expr          ::= (NOT)* term ((PLUS | MINUS | CMP_OP | AND | OR) term)*

    term          ::= factor ((MUL | DIV) factor)*

    factor        ::= NUM
                  |   PLUS NUM
                  |   MINUS NUM
                  |   ID
                  |   '(' expr ')'

    compound_stmt ::= BEGIN (stmt SEMICOLON)* END

    stmt          ::= compound_stmt
                  |   if_stmt
                  |   while_stmt
                  |   assign_stmt
                  |   return_stmt

    assign_stmt   ::= ID ASSIGN expr SEMICOLON

    if_stmt       ::= IF expr THEN compound_stmt
                  |   IF expr THEN compound_stmt ELSE compound_stmt

    while_stmt    ::= WHILE expr DO compound_stmt

    for_stmt      ::= FOR variable IN variable DO compound_stmt

    return_stmt   ::= RETURN expr

    function      ::= DEF function_name '(' arg_list ')' compound_stmt

    params        ::= param_list*

    param_list    ::= ID (',' ID)*

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
        elif token.tag == ID:
            return IdAST(self.consume().val)
        elif token.tag == RESERVED:
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
        """expr ::= term ((PLUS | MINUS | ...) term)*"""
        expr_ast = self.term()

        token = self.peek()
        while token is not None and token.tag == RESERVED and \
                (token.val == '+' or token.val == '-' or
                 token.val == '>' or token.val == '<' or
                 token.val == '>=' or token.val == '<=' or
                 token.val == 'and' or token.val == 'or'):
            op = self.consume()
            right = self.term()
            new_ast = BinaryOPAST(op.val, expr_ast, right)
            expr_ast = new_ast
            token = self.peek()

        return expr_ast

    def assign_stmt(self):
        stmt = None
        id_token = self.consume()
        eq_token = self.peek()

        if eq_token is not None and eq_token.tag == RESERVED and \
                eq_token.val == '=':
            self.consume()
            val_ast = self.expr()
            stmt = AssignAST(IdAST(id_token.val), val_ast)

        token = self.peek()
        if token is not None and token.tag == RESERVED and \
                token.val == ';':
            self.consume()
        else:
            raise Exception('a semicolon is need')

        return stmt

    def if_stmt(self):
        """if_stmt   ::= IF expr THEN compound_stmt
                     |   IF expr THEN compound_stmt ELSE compound_stmt
        """
        if_stmt = None
        token = self.peek()
        if token.tag == RESERVED and token.val == 'if':
            self.consume()
            cond = self.expr()
            token = self.peek()
            if token.tag == RESERVED and token.val == 'then':
                self.consume()
                then = self.compound_stmt()
                token = self.peek()
                if token.tag == RESERVED and token.val == 'else':
                    self.consume()
                    els = self.compound_stmt()
                    if_stmt = IfAST(cond, then, els)
                else:
                    if_stmt = IfAST(cond, then, None)
            else:
                raise Exception('if need a then')

        return if_stmt

    def while_stmt(self):
        """while_stmt    ::= WHILE expr DO compound_stmt"""
        while_stmt = None
        token = self.peek()
        if token.tag == RESERVED and token.val == 'while':
            self.consume()
            cond = self.expr()
            token = self.peek()
            if token.tag == RESERVED and token.val == 'do':
                self.consume()
                then = self.compound_stmt()
                while_stmt = WhileAST(cond, then)
            else:
                raise Exception('broken while statement, need a `do`')

        return while_stmt

    def for_stmt(self):
        """for_stmt      ::= FOR variable IN expr DO compound_stmt"""
        for_stmt = None
        token = self.peek()
        if token.tag == RESERVED and token.val == 'for':
            self.consume()
            token = self.peek()
            if token.tag == ID:
                item = IdAST(self.consume().val)
                token = self.peek()
                if token.tag == RESERVED and token.val == 'in':
                    self.consume()
                    items = self.expr()
                    token = self.peek()
                    if token.tag == RESERVED and token.val == 'do':
                        self.consume()
                        then = self.compound_stmt()
                        for_stmt = ForAST(item, items, then)
                else:
                    raise Exception('broken for statement, need a items variable')
            else:
                raise Exception('bad for statements: need a item variable')

        return for_stmt

    def stmt(self):
        """stmt   ::= compound_stmt
                  |   if_stmt
                  |   while_stmt
                  |   assign_stmt
                  |   for_stmt
                  |   empty
        """
        stmt = None
        token = self.peek()

        if token is not None:
            if token.tag == ID:
                stmt = self.assign_stmt()
            elif token.val == 'if':
                stmt = self.if_stmt()
            elif token.val == 'while':
                stmt = self.while_stmt()
            elif token.val == 'for':
                stmt = self.for_stmt()

        return stmt

    def compound_stmt(self):
        """compound_stmt ::= BEGIN (stmt SEMICOLON)* END"""
        stmts = CompoundStmtASt()

        token = self.peek()
        if token is not None and token.tag == RESERVED and \
                token.val == 'begin':
            self.consume()

            while True:
                stmt = self.stmt()
                if stmt is None:
                    break
                stmts.add(stmt)

            token = self.peek()
            if token is not None and token.tag == RESERVED and \
                    token.val == 'end':
                self.consume()
            else:
                raise Exception('no end found')

        return stmts

    def identifier(self):
        token = self.peek()
        if token.tag == ID:
            token = self.consume()
            return IdAST(token.val)
        else:
            raise Exception('not an identifier')

    def match(self, val):
        """ if the next token is identical to val, then consume the token,
        raise a Exception otherwise
        """
        token = self.peek()
        if token.tag == RESERVED and token.val == val:
            self.consume()
        else:
            raise Exception('match failed: {}'.format(val))

    def params(self):
        """ params        ::= param_list? """
        args = []
        token = self.peek()

        if token.tag == ID:
            args = self.param_list()

        return args

    def param_list(self):
        """ param_list    ::= ID (',' ID)* """
        args = []
        arg = self.identifier()
        args.append(arg)
        token = self.peek()
        while token.tag == RESERVED and token.val == ',':
            self.consume()
            arg = self.identifier()
            args.append(arg)
            token = self.peek()

        return args

    def function_stmt(self):
        """
        function      ::= DEF function_name '(' arg_list ')' compound_stmt
        """
        self.match('def')
        func_name = self.identifier()
        self.match('(')
        func_args = self.params()
        self.match(')')
        func_body = self.compound_stmt()
        return FunctionAST(func_name, func_args, func_body, None)

    def parse(self):
        token = self.peek()
        if token.val == 'def':
            return self.function_stmt()
        else:
            return self.compound_stmt()
