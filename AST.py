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
        self.value = value

    def __repr__(self, level=0):
        return '\t' * level + repr(self.value) + '\n'


class UnaryOPAST(AST):
    def __init__(self, op, value):
        self.op = op
        self.value = value

    def __repr__(self, level=0):
        return '\t' * level + repr(self.op) + self.value.__repr__(level) + '\n'
