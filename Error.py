class ExpressionTypeError(Exception):
    def __init__(self, line, op, type1, type2):
        if type2 is not None:
            msg = 'line {}: Operação {} não suportada para tipos {} e {}'.format(line, op, type1, type2)
        else:
            msg = 'line {}: Operação {} não suportada para o tipo {}'.format(line, op, type1)
        super().__init__(msg)


class UndeclaredVariable(Exception):
    def __init__(self, line, name):
        msg = 'line {}: Variável {} não declarada'. format(line, name)
        super().__init__(msg)


class UndeclaredFunction(Exception):
    def __init__(self, line, name):
        msg = 'line {}: Função {} não foi declarada'. format(line, name)
        super().__init__(msg)


class UnexpectedTypeError(Exception):
    def __init__(self, line, type1, type2):
        msg = 'line {}: Esperava tipo {} mas recebeu tipo {}'.format(line, type1, type2)
        super().__init__(msg)


class UnexpectedArgumentTypeError(Exception):
    def __init__(self, line, type1, type2):
        msg = 'line {}: Função esperava argumento do tipo {}, mas recebeu {}'.format(line, type1, type2)
        super().__init__(msg)


class UnexpectedReturnTypeError(Exception):
    def __init__(self, line, type1, type2):
        msg = 'line {}: Função esperava retorno do tipo {}, recebeu {}'.format(line, type1, type2)
        super().__init__(msg)


class AlreadyDeclaredError(Exception):
    def __init__(self, line, name):
        msg = 'line {}: Variável com nome {} já foi declarada'.format(line, name)
        super().__init__(msg)


class AlreadyDeclaredFunctionError(Exception):
    def __init__(self, line, name):
        msg = 'line {}: Função ou variável global ou constante com nome {} já foi declarada'.format(line, name)
        super().__init__(msg)


class ReservedError(Exception):
    def __init__(self, line, reserved):
        msg = 'line {}: Palavra reservada {} não pode ser usada como nome de variável'.format(line, reserved)
        super().__init__(msg)


class MissingArguments(Exception):
    def __init__(self, line, esperado, recebido):
        msg = 'line {}: A função esperava {} argumentos, mas recebeu {}'.format(line, esperado, recebido)
        super().__init__(msg)


class UnexpectedReturn(Exception):
    def __init__(self, line):
        msg = 'line {}: return fora do escopo de uma função'.format(line)
        super().__init__(msg)


class UnexpectedBreak(Exception):
    def __init__(self, line):
        msg = 'line {}: break fora do escopo de um laço de repetição'.format(line)
        super().__init__(msg)