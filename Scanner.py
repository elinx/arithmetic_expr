import re


RESERVED = 'RESERVED'
INT = 'INT'
ID = 'ID'

tokens_exprs = [
    (r'[ \n\t]+',               None),
    (r'\(',                    'RESERVED'),
    (r'\)',                    'RESERVED'),
    (r'\+',                    'RESERVED'),
    (r'-',                     'RESERVED'),
    (r'\*',                    'RESERVED'),
    (r'\/',                    'RESERVED'),
    (r'\d+',                   'INT'),
    (r'[A-Za-z][A-Za-z0-9_]*', 'ID'),
]


class Token:
    def __init__(self, val, tag):
        self.val = val
        self.tag = tag

    def __repr__(self):
        return '({}, {})'.format(self.val, self.tag)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class Scanner:

    def __init__(self, inputs):
        self.inputs = inputs
        self.tokens = []
        self.pos = 0

    def lex(self):
        while self.pos < len(self.inputs):
            match = None
            for tokens_expr in tokens_exprs:
                pattern, tag = tokens_expr
                regex = re.compile(pattern)
                match = regex.match(self.inputs, self.pos)
                if match:
                    val = match.group(0)
                    if tag:
                        self.tokens.append(Token(val, tag))
                    break
            if not match:
                raise ValueError('inputs {} is not valid.'.format(self.inputs[self.pos]))
            else:
                self.pos = match.end(0)
