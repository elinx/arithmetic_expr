# Add function support
1. add a `def` token to `tokens_exprs` list

```python
tokens_exprs = [
    (r'def',                    RESERVED)
]
```

2. add grammars for function parsing
```BNF
    function      ::= DEF function_name '(' arg_list ')' compound_stmt

    params        ::= param_list*

    param_list    ::= ID (',' ID)*
```

3. add parsing codes
```python
    def params(self):
        """ params        ::= param_list? """
        args = []
        token = self.peek()

        if token.tag == ID:
            args = self.param_list()

        return args

    def param_list(self):
        """ param_list    ::= ID (',' ID)* """
        args = []
        arg = self.identifier()
        args.append(arg)
        token = self.peek()
        while token.tag == RESERVED and token.val == ',':
            self.consume()
            arg = self.identifier()
            args.append(arg)
            token = self.peek()

        return args

    def function_stmt(self):
        """
        function      ::= DEF function_name '(' arg_list ')' compound_stmt
        """
        self.match('def')
        func_name = self.identifier()
        self.match('(')
        func_args = self.params()
        self.match(')')
        func_body = self.compound_stmt()
        return FunctionAST(func_name, func_args, func_body, None)

```

4. Add Function AST to store function information
```python
class FunctionAST(AST):
    def __init__(self, name, args, body, ret):
        self.name = name
        self.args = args
        self.body = body
        self.ret = ret

    def __eq__(self, other):
        return self.name == other.name and \
               self.args == other.args and \
               self.body == other.body and \
               self.ret == other.ret
```

5. add test case for parsing and lex code

6. add visitor method to eval function
```python
    def visitFunctionAst(self, node, env):
        pass
```