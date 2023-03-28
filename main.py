from antlr4 import *

from gen.trabalhoFinalParser import trabalhoFinalParser
from gen.trabalhoFinalLexer import trabalhoFinalLexer
from trabalhoFinalMyListener import trabalhoFinalMyListener

if __name__ == '__main__':
    data = FileStream('exemplo.py')
    lexer = trabalhoFinalLexer(data)
    stream = CommonTokenStream(lexer)

    parser = trabalhoFinalParser(stream)
    tree = parser.prog()

    l = trabalhoFinalMyListener()
    walker = ParseTreeWalker()
    walker.walk(l, tree)
