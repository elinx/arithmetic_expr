class Env:
    def __init__(self):
        self.syms = {}

    def add(self, sym):
        self.syms[sym.name] = sym

    def remove(self, sym):
        pass

    def search(self, name):
        if name in self.syms:
            return self.syms[name]
        else:
            return None

    def update(self, sym):
        self.syms[sym.name] = sym