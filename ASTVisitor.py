from AST import *


class ASTVisitor:

    def __init__(self):
        pass

    def visit(self, ast):
        method_key = 'visit' + type(ast).__name__
        visit_method = getattr(self, method_key, self.generic_visit)
        return visit_method(ast)

    def generic_visit(self, ast):
        raise Exception('no visit method for {}'.format(type(ast).__name__))


class ASTDisplayVisitor(ASTVisitor):
    def __init__(self):
        pass

    def visitBinaryOPAST(self, node):
        return repr(node)

    def visitIntegerAST(self, node):
        return repr(node)

    def display(self, ast):
        print(self.visit(ast))


class ASTEvalVisitor(ASTVisitor):

    def __init__(self):
        pass

    def visitBinaryOPAST(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        return {
            '+': left + right,
            '-': left - right,
            '*': left * right,
            '/': left / right
        }[node.value]

    def visitIntegerAST(self, node):
        return node.value

    def eval(self, ast):
        return self.visit(ast)