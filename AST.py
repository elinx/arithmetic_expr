class AST(object):

    def accept(self, visitor):
        pass


class BinaryOPAST(AST):
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


class IntegerAST(AST):
    def __init__(self, value):
        self.value = value

    def __repr__(self, level):
        return '\t' * level + str(self.value) + '\n'

