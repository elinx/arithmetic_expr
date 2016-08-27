Thanks to the [Let’s Build A Simple Interpreter](https://ruslanspivak.com/lsbasi-part1/) series
I build a simple interpreter which can parse and evaluate basic arithmetic expression and
basic `if` and `while` statements.

Here, the compound statements are a bunch of statements each end with a semicolon. To `eval` them,
a simple symbol table is created used as `enviroment` for data reference. You can see the code
just use a flat table, when the `eval` procedure meets a assignment statement, it will update
the symbol table, also a search interface is provided to check whether the symbol is in the symbol
table.

So far so good, and every thing is simple. Next, I'll add function support.
