from Symbol import *


class Scope:
    def __init__(self, name, parent):
        self.name = name
        self.syms = []
        self.parent = parent

    def resolve(self, name):
        pass