import re


RESERVED = 'RESERVED'
INT = 'INT'
ID = 'ID'

tokens_exprs = [
    (r'[ \n\t]+',               None),
    (r'[0-9]+[a-zA-Z_]+',       None),
    (r'begin',                  RESERVED),
    (r'end',                    RESERVED),
    (r'if',                     RESERVED),
    (r'then',                   RESERVED),
    (r'else',                   RESERVED),
    (r'while',                  RESERVED),
    (r'for',                    RESERVED),
    (r'in',                     RESERVED),
    (r'do',                     RESERVED),
    (r'and',                    RESERVED),
    (r'or',                     RESERVED),
    (r'not',                    RESERVED),
    (r'\(',                     RESERVED),
    (r'\)',                     RESERVED),
    (r'\+',                     RESERVED),
    (r'-',                      RESERVED),
    (r'\*',                     RESERVED),
    (r'\/',                     RESERVED),
    (r'>=',                     RESERVED),
    (r'<=',                     RESERVED),
    (r'==',                     RESERVED),
    (r'!=',                     RESERVED),
    (r'>',                      RESERVED),
    (r'<',                      RESERVED),
    (r'=',                      RESERVED),
    (r';',                      RESERVED),
    (r'\d+',                    INT),
    (r'[A-Za-z][A-Za-z0-9_]*',  ID),
]


class Token:
    def __init__(self, val, tag):
        self.val = val
        self.tag = tag

    def __repr__(self):
        return '({}, {})'.format(self.val, self.tag)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class UnacceptableInput(Exception):
    pass


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
                raise UnacceptableInput('inputs {} is not valid.'.format(self.inputs[self.pos]))
            else:
                self.pos = match.end(0)

        if not self.tokens:
            raise UnacceptableInput(self.inputs)
