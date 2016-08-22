from Type import *


class Symbol:
    def __init__(self, name, type):
        self.name = name
        self.type = type


class VariableSymbol(Symbol):
    def __init__(self, name, type):
        super(name, type)


class BuiltInSymbol(Symbol):
    def __init__(self, name):
        super(name)
