from AST import *
from Env import *
from Symbol import *


class ASTVisitor:

    def __init__(self):
        pass

    def visit(self, ast, env):
        method_key = 'visit' + type(ast).__name__
        visit_method = getattr(self, method_key, self.generic_visit)
        return visit_method(ast, env)

    def generic_visit(self, ast):
        raise Exception('no visit method for {}'.format(type(ast).__name__))


class ASTDisplayVisitor(ASTVisitor):
    def __init__(self):
        pass

    def visitBinaryOPAST(self, node):
        return repr(node)

    def visitUnaryOPAST(self, node):
        return repr(node.op) + repr(node.value)

    def visitIntegerAST(self, node):
        return repr(node)

    def display(self, ast):
        print(self.visit(ast))


class ASTEvalVisitor(ASTVisitor):

    def __init__(self):
        pass

    def visitBinaryOPAST(self, node, env):
        left = self.visit(node.left, env)
        right = self.visit(node.right, env)

        return {
            '+': left + right,
            '-': left - right,
            '*': left * right,
            '/': left / right,
            '>': left > right
        }[node.op]

    def visitUnaryOPAST(self, node):
        return {
            '+': self.visit(node.value),
            '-': -self.visit(node.value)
        }[node.op]

    def visitIdAST(self, node, env):
        sym = env.search(node.name)
        if sym is not None:
            return sym.val
        else:
            return None

    def visitIntegerAST(self, node, env):
        return node.value

    def visitAssignAST(self, node, env):
        env.add(Symbol(node.id.name, type(node.val), node.val))

    def visitCompoundStmtASt(self, node, env):
        for stmt in node.stmts:
            self.visit(stmt, env)

    def visitIfAST(self, node, env):
        if self.visit(node.cond, env):
            self.visit(node.then, env)
        else:
            self.visit(node.els, env)
            print(env)

    def visitFunctionAst(self, node, env):
        pass

    def eval(self, ast):
        return self.visit(ast, Env())
