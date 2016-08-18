class AST(object):

    def accept(self, visitor):
        pass


class BinaryOPAST(AST):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self, level=0):
        ret = '\t' * level + repr(self.op) + '\n'
        if self.left is not None:
            ret += self.left.__repr__(level + 1)
        if self.right is not None:
            ret += self.right.__repr__(level + 1)
        return ret


class IntegerAST(AST):
    def __init__(self, value):
        """value is an integer"""
        self.value = value

    def __repr__(self, level=0):
        return '\t' * level + repr(self.value) + '\n'

    def __eq__(self, other):
        return self.value == other.value


class UnaryOPAST(AST):
    def __init__(self, op, value):
        self.op = op
        self.value = value

    def __repr__(self, level=0):
        return '\t' * level + repr(self.op) + self.value.__repr__(level) + '\n'


class CompoundStmtASt(AST):
    def __init__(self, *args):
        self.stmts = []
        for stmt in args:
            self.stmts.append(stmt)

    def __eq__(self, other):
        res = True
        for stmt in self.stmts:
            if stmt not in other.stmts:
                res = False
        return res

    def add(self, stmt):
        if stmt is not None:
            self.stmts.append(stmt)


class AssignAST(AST):
    def __init__(self, id, value):
        self.id = id
        self.value = value

    def __repr__(self, level=0):
        return '\t' * level + repr(self.id) + self.value.__repr__(level) + '\n'

    def __eq__(self, other):
        return self.id == other.id and self.value == self.value


class IfAST(AST):
    def __init__(self, expr, stmts):
        self.expr = expr
        self.stmts = stmts


class WhileAST(AST):
    def __init__(self, expr, stmts):
        self.expr = expr
        self.stmts = stmts


class ForAST(AST):
    pass
