from Type import *


class Symbol:
    def __init__(self, name, type, val):
        self.name = name
        self.type = type
        self.val = val

    def __repr__(self):
        return 'name: {}, type: {}, val: {}'.format(self.name, self.type, self.val)


class VariableSymbol(Symbol):
    def __init__(self, name, type, val):
        super(name, type, val)


class BuiltInSymbol(Symbol):
    def __init__(self, name, val):
        super(name)
