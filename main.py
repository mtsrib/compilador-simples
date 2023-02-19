from antlr4 import *

from gen.trabalhoFinalParser import trabalhoFinalParser
from gen.trabalhoFinalLexer import trabalhoFinalLexer
from trabalhoFinalMyListener import trabalhoFinalMyListener

if __name__ == '__main__':
    data = FileStream('input.txt')
    lexer = trabalhoFinalLexer(data)
    stream = CommonTokenStream(lexer)

    parser = trabalhoFinalParser(stream)
    tree = parser.prog()

    m = trabalhoFinalMyListener()
    walker = ParseTreeWalker()
    walker.walk(m, tree)
