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

    def __eq__(self, other):
        return self.op == other.op and  \
               self.left == other.left and  \
               self.right == other.right


class IntegerAST(AST):
    def __init__(self, value):
        """value is an integer"""
        self.value = value

    def __repr__(self, level=0):
        return '\t' * level + repr(self.value) + '\n'

    def __eq__(self, other):
        return self.value == other.value

    def __add__(self, other):
        return self.value + other.value

    def __sub__(self, other):
        return self.value - other.value

    def __mul__(self, other):
        return self.value * other.value

    def __truediv__(self, other):
        return self.value / other.value

    def __gt__(self, other):
        return self.value > other.value


class IdAST(AST):
    def __init__(self, name):
        self.name = name

    def __repr__(self, level=0):
        return '\t' * level + repr(self.name) + '\n'

    def __eq__(self, other):
        return self.name == other.name


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
        return self.stmts == other.stmts

    def add(self, stmt):
        if stmt is not None:
            self.stmts.append(stmt)


class AssignAST(AST):
    def __init__(self, id, val):
        self.id = id
        self.val = val

    def __repr__(self, level=0):
        return '\t' * level + repr(self.id) + self.val.__repr__(level) + '\n'

    def __eq__(self, other):
        return self.id == other.id and self.val == self.val


class IfAST(AST):
    def __init__(self, cond, then, els=None):
        self.cond = cond
        self.then = then
        self.els = els

    def __eq__(self, other):
        return self.cond == other.cond and \
               self.then == other.then and \
               self.els == other.els


class WhileAST(AST):
    def __init__(self, cond, then):
        self.cond = cond
        self.then = then

    def __eq__(self, other):
        return self.cond == other.cond and \
               self.then == other.then


class ForAST(AST):
    def __init__(self, item, items, do):
        self.item = item
        self.items = items
        self.do = do

    def __eq__(self, other):
        return self.item == other.item and \
               self.items == other.items and \
               self.do == other.do
