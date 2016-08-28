class Env:
    def __init__(self):
        self.syms = {}

    def __repr__(self):
        ret = ''
        i = 0
        for k, v in self.syms.items():
            ret += '[{}] {} => {}'.format(str(i), repr(k), repr(v))
            i += 1
        return ret

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