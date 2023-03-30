from antlr4 import *
from gen.trabalhoFinalParser import trabalhoFinalParser
from gen.trabalhoFinalListener import trabalhoFinalListener
from Error import *


# Definicao da classe MyListener.
class trabalhoFinalMyListener(trabalhoFinalListener):
    # tabela de símbolos glogal
    # {id : [tipo, valor]}
    symbolTable = {}

    # tabela de símbolos local
    # {id : [tipo, valor]}
    symbolTableLocal = {}

    # O dicionário abaixo guarda os identificadores das funções e os tipos dos parâmetros formais da função
    # {id_func : [tipos]}
    f_args = {}

    stack = []
    active_function = []
    reserved = ["'True'", "'False'", "'if'", "'else'", "'for'", "'while'", "'print'", "'input'", "'int'",
                "'real'", "'String'", "'boolean'", "'main'", "'return'", "'break'", "'const'"]

    def numeric_type(self, vtype):  # função que verifica se é um tipo numério
        return (vtype == 'int') or (vtype == 'real')

    def _active_function(self):
        return 'function' in self.stack

    # Enter a parse tree produced by projetoFinalParser#prog.
    def enterProg(self, ctx: trabalhoFinalParser.ProgContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#prog.
    def exitProg(self, ctx: trabalhoFinalParser.ProgContext):
        print("\nTabela de símbolos")
        print(self.symbolTable)
        print("\nTabela de símbolos local")
        print(self.symbolTableLocal)

    # Enter a parse tree produced by trabalhoFinalParser#decVarConst.
    def enterDecVarConst(self, ctx: trabalhoFinalParser.DecVarConstContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#decVarConst.
    def exitDecVarConst(self, ctx: trabalhoFinalParser.DecVarConstContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#decConst.
    def enterDecConst(self, ctx: trabalhoFinalParser.DecConstContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#decConst.
    def exitDecConst(self, ctx: trabalhoFinalParser.DecConstContext):
        flag = 0
        variaveis = ctx.listaAtrib().listaids
        tipos = ctx.listaAtrib().listatipos

        for i in range(len(variaveis)):
            if ctx.tipo().getText() != tipos[i]:
                flag = 1
                raise UnexpectedTypeError(ctx.start.line, ctx.tipo().getText(), tipos[i])

        if flag == 0:
            for var in variaveis:
                self.symbolTable[var][0] = ctx.tipo().getText()

        for var in variaveis:  # atualiza a tabela de símbolos para armazenar valores realmente inteiros e floats
            if ctx.tipo().getText() == 'int':
                self.symbolTable[var][1] = int(self.symbolTable[var][1])
            elif ctx.tipo().getText() == 'real':
                self.symbolTable[var][1] = float(self.symbolTable[var][1])

    # Enter a parse tree produced by trabalhoFinalParser#decVar.
    def enterDecVar(self, ctx: trabalhoFinalParser.DecVarContext):
        pass

        # Exit a parse tree produced by trabalhoFinalParser#decVar.

    def exitDecVar(self, ctx: trabalhoFinalParser.DecVarContext):
        variaveis = ctx.listaIds().lista

        # valor padrão das variáveis
        for var in variaveis:
            self.symbolTable[var][0] = ctx.tipo().getText()
            if ctx.tipo().getText() == 'String':
                self.symbolTable[var][1] = "''"
            elif self.numeric_type(ctx.tipo().getText()):
                self.symbolTable[var][1] = 0
            elif ctx.tipo().getText() == 'boolean':
                self.symbolTable[var][1] = 'False'

    # Enter a parse tree produced by trabalhoFinalParser#tipo.
    def enterTipo(self, ctx: trabalhoFinalParser.TipoContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#tipo.
    def exitTipo(self, ctx: trabalhoFinalParser.TipoContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#listaIds.
    def enterListaIds(self, ctx: trabalhoFinalParser.ListaIdsContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#listaIds.
    def exitListaIds(self, ctx: trabalhoFinalParser.ListaIdsContext):
        ids = []
        for token in ctx.ID():
            if token.getText() in self.reserved:
                raise ReservedError(ctx.start.line, token.getText())

            elif token.getText().lower() in self.symbolTable:
                raise AlreadyDeclaredError(ctx.start.line, token.getText())

            else:
                ids.append(token.getText().lower())

        for i in range(len(ids)):
            self.symbolTable[ctx.ID(i).getText().lower()] = [None, None]

        ctx.lista = ids

    # Enter a parse tree produced by trabalhoFinalParser#listaAtrib.
    def enterListaAtrib(self, ctx: trabalhoFinalParser.ListaAtribContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#listaAtrib.
    def exitListaAtrib(self, ctx: trabalhoFinalParser.ListaAtribContext):
        valores = []
        tipos = []
        ids = []

        for valor in ctx.valor():
            valores.append(valor.getText())  # preenche a lista de valores
            tipos.append(valor.type)  # preenche a lista de tipos

        for token in ctx.ID():
            if token.getText().lower() in self.symbolTable:
                raise AlreadyDeclaredError(ctx.start.line, token.getText())

            elif token.getText() in self.reserved:
                raise ReservedError(ctx.start.line, token.getText())

            else:
                ids.append(token.getText().lower())

        for i in range(len(ids)):
            self.symbolTable[ctx.ID(i).getText().lower()] = [None, valores[i]]

        ctx.listaids = ids
        ctx.listatipos = tipos

    # Enter a parse tree produced by trabalhoFinalParser#ValorInteiro.
    def enterValorInteiro(self, ctx: trabalhoFinalParser.ValorInteiroContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#ValorInteiro.
    def exitValorInteiro(self, ctx: trabalhoFinalParser.ValorInteiroContext):
        ctx.type = 'int'
        if '-' in ctx.getText():
            ctx.val = - int(ctx.INT().getText())
        else:
            ctx.val = int(ctx.INT().getText())

    # Enter a parse tree produced by trabalhoFinalParser#ValorReal.
    def enterValorReal(self, ctx: trabalhoFinalParser.ValorRealContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#ValorReal.
    def exitValorReal(self, ctx: trabalhoFinalParser.ValorRealContext):
        ctx.type = 'real'
        if '-' in ctx.getText():
            ctx.val = - float(ctx.REAL().getText())  # número real negativo
        else:
            ctx.val = float(ctx.REAL().getText())

    # Enter a parse tree produced by trabalhoFinalParser#ValorString.
    def enterValorString(self, ctx: trabalhoFinalParser.ValorStringContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#ValorString.
    def exitValorString(self, ctx: trabalhoFinalParser.ValorStringContext):
        ctx.type = 'String'
        ctx.val = ctx.STR().getText()

    # Enter a parse tree produced by trabalhoFinalParser#ValorBool.
    def enterValorBool(self, ctx: trabalhoFinalParser.ValorBoolContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#ValorBool.
    def exitValorBool(self, ctx: trabalhoFinalParser.ValorBoolContext):
        ctx.type = 'boolean'
        ctx.val = ctx.BOOL().getText()

    # Enter a parse tree produced by trabalhoFinalParser#Func_Type.
    def enterFunc_Type(self, ctx: trabalhoFinalParser.Func_TypeContext):

        self.stack.append('function')  # adiciona na pilha de execução
        func_id = ctx.ID().getText()
        self.active_function.append(func_id)  # adiciona na lista de função ativa

        # add a função na tabela de símboloos
        if func_id in self.symbolTable:
            raise AlreadyDeclaredFunctionError(ctx.start.line, func_id)
        else:
            if ctx.tipoFun().getText() != '':
                self.symbolTable[func_id] = [ctx.tipoFun().getText(), None]
            else:
                self.symbolTable[func_id] = [None, None]  # caso a função não tenha tipo

        if self.numeric_type(self.symbolTable[func_id][0]):
            self.symbolTable[func_id][1] = 0
        elif self.symbolTable[func_id][0] == 'String':
            self.symbolTable[func_id][1] = "''"
        elif self.symbolTable[func_id][0] == 'boolean':
            self.symbolTable[func_id][1] = 'False'

        tipos = []
        stream = ctx.listaParams().getText()
        splitstream = stream.split(",")
        for token in splitstream:
            if 'int' in token:
                tipos.append('int')
            elif 'real' in token:
                tipos.append('real')
            elif 'boolean' in token:
                tipos.append('boolean')
            elif 'String' in token:
                tipos.append('String')

        self.f_args[func_id] = tipos

    # Exit a parse tree produced by trabalhoFinalParser#Func_Type.
    def exitFunc_Type(self, ctx: trabalhoFinalParser.Func_TypeContext):
        self.stack.pop()  # retira da pilha de execução
        self.active_function.pop()  # retira da lista de função ativa

    # Enter a parse tree produced by trabalhoFinalParser#decVarLocal.
    def enterDecVarLocal(self, ctx: trabalhoFinalParser.DecVarLocalContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#decVarLocal.
    def exitDecVarLocal(self, ctx: trabalhoFinalParser.DecVarLocalContext):
        variaveis = ctx.listaIdsLocal().lista

        # valor padrão das variáveis
        for var in variaveis:
            self.symbolTableLocal[var][0] = ctx.tipo().getText()
            if ctx.tipo().getText() == 'String':
                self.symbolTableLocal[var][1] = "''"
            elif self.numeric_type(ctx.tipo().getText()):
                self.symbolTableLocal[var][1] = 0
            elif ctx.tipo().getText() == 'boolean':
                self.symbolTableLocal[var][1] = 'False'

    # Enter a parse tree produced by trabalhoFinalParser#listaIdsLocal.
    def enterListaIdsLocal(self, ctx: trabalhoFinalParser.ListaIdsLocalContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#listaIdsLocal.
    def exitListaIdsLocal(self, ctx: trabalhoFinalParser.ListaIdsLocalContext):
        ids = []
        for token in ctx.ID():
            if token.getText() in self.reserved:
                raise ReservedError(ctx.start.line, token.getText())

            elif token.getText().lower() in self.symbolTableLocal:
                raise AlreadyDeclaredError(ctx.start.line, token.getText())

            else:
                ids.append(token.getText().lower())

        for i in range(len(ids)):
            self.symbolTableLocal[ctx.ID(i).getText().lower()] = [None, None]

        ctx.lista = ids

    # Enter a parse tree produced by trabalhoFinalParser#tipoFun.
    def enterTipoFun(self, ctx: trabalhoFinalParser.TipoFunContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#tipoFun.
    def exitTipoFun(self, ctx: trabalhoFinalParser.TipoFunContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#listaParams.
    def enterListaParams(self, ctx: trabalhoFinalParser.ListaParamsContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#listaParams.
    def exitListaParams(self, ctx: trabalhoFinalParser.ListaParamsContext):
        ids = []
        types = []

        for token in ctx.tipo():
            types.append(token.getText())

        for token in ctx.ID():
            if token.getText() in self.symbolTableLocal:
                raise AlreadyDeclaredError(ctx.start.line, token.getText())

            elif token.getText() in self.reserved:
                raise ReservedError(ctx.start.line, token.getText())
            else:
                ids.append(token.getText())

        for i in range(len(ids)):
            self.symbolTableLocal[ctx.ID(i).getText()] = [types[i], None]

        for var in ids:
            if self.symbolTableLocal[var][0] == 'String':
                self.symbolTableLocal[var][1] = "''"
            elif self.numeric_type(self.symbolTableLocal[var][0]):
                self.symbolTableLocal[var][1] = 0
            elif self.symbolTableLocal[var][0] == 'boolean':
                self.symbolTableLocal[var][1] = 'False'

    # Enter a parse tree produced by trabalhoFinalParser#main.
    def enterMain(self, ctx: trabalhoFinalParser.MainContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#main.
    def exitMain(self, ctx: trabalhoFinalParser.MainContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#comandos.
    def enterComandos(self, ctx: trabalhoFinalParser.ComandosContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#comandos.
    def exitComandos(self, ctx: trabalhoFinalParser.ComandosContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#comandosRep.
    def enterComandosRep(self, ctx: trabalhoFinalParser.ComandosRepContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#comandosRep.
    def exitComandosRep(self, ctx: trabalhoFinalParser.ComandosRepContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#callF.
    def enterCallF(self, ctx: trabalhoFinalParser.CallFContext):
        id_name = ctx.ID().getText()
        if id_name not in self.symbolTable:  # testa se o identificar da função não está na tabela de símbolos
            raise UndeclaredFunction(ctx.start.line, id_name)

    # Exit a parse tree produced by trabalhoFinalParser#callF.
    def exitCallF(self, ctx: trabalhoFinalParser.CallFContext):
        fun_id = ctx.ID().getText()
        if len(self.f_args[fun_id]) != len(
                ctx.expr()):  # testa se o número de argumentos passados é diferente do número de parâmetros formais
            raise MissingArguments(ctx.start.line, len(self.f_args[fun_id]), len(ctx.expr()))
        else:
            for esperado, recebido in list(zip(self.f_args[fun_id],
                                               ctx.expr())):  # testa se os tipos dos parâmetros formais correspondem aos valores recebidos por argumento
                if esperado != recebido.type:
                    raise UnexpectedArgumentTypeError(ctx.start.line, esperado, recebido.type)
                else:
                    ctx.type = self.symbolTable[ctx.ID().getText()][0]  # tipo da função
                    ctx.val = self.symbolTable[ctx.ID().getText()][1]  # valor retornado pela função


    # Enter a parse tree produced by trabalhoFinalParser#Expr_Arit.
    def enterExpr_Arit(self, ctx: trabalhoFinalParser.Expr_AritContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#Expr_Arit.
    def exitExpr_Arit(self, ctx: trabalhoFinalParser.Expr_AritContext):
        ctx.type = ctx.exprArit().type
        ctx.val = ctx.exprArit().val

    # Enter a parse tree produced by trabalhoFinalParser#Expr_Bool.
    def enterExpr_Rel(self, ctx: trabalhoFinalParser.Expr_RelContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#Expr_Bool.
    def exitExpr_Rel(self, ctx: trabalhoFinalParser.Expr_RelContext):
        ctx.type = ctx.exprRel().type
        ctx.val = ctx.exprRel().val

    # Enter a parse tree produced by trabalhoFinalParser#Termo_Arit.
    def enterTermo_Arit(self, ctx: trabalhoFinalParser.Termo_AritContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#Termo_Arit.
    def exitTermo_Arit(self, ctx: trabalhoFinalParser.Termo_AritContext):
        ctx.type = ctx.termoArit().type
        ctx.val = ctx.termoArit().val

    # Enter a parse tree produced by trabalhoFinalParser#SomaSub.
    def enterSomaSub(self, ctx: trabalhoFinalParser.SomaSubContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#SomaSub.
    def exitSomaSub(self, ctx: trabalhoFinalParser.SomaSubContext):
        if self.numeric_type(ctx.exprArit().type) and self.numeric_type(
                ctx.termoArit().type):  # verifica se os dois operandos são numéricos
            if ctx.exprArit().type == 'real' and ctx.termoArit().type == 'real':
                ctx.type = 'real'
                v1, v2 = ctx.exprArit().val, ctx.termoArit().val  # recebe os valores dos operanddos

            elif ctx.exprArit().type == 'int' and ctx.termoArit().type == 'real':
                ctx.type = 'real'  # conversão de alargamento
                v1, v2 = float(ctx.exprArit().val), ctx.termoArit().val

            elif ctx.exprArit().type == 'real' and ctx.termoArit().type == 'int':
                ctx.type = 'real'
                v1, v2 = ctx.exprArit().val, float(ctx.termoArit().val)
            else:
                ctx.type = 'int'
                v1, v2 = ctx.exprArit().val, ctx.termoArit().val

            if ctx.op.text == '+':
                ctx.val = v1 + v2
            else:
                ctx.val = v1 - v2
        else:
            raise ExpressionTypeError(ctx.start.line, ctx.op.text, ctx.exprArit().type, ctx.termoArit().type)

    # Enter a parse tree produced by trabalhoFinalParser#Fator_Arit.
    def enterFator_Arit(self, ctx: trabalhoFinalParser.Fator_AritContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#Fator_Arit.
    def exitFator_Arit(self, ctx: trabalhoFinalParser.Fator_AritContext):
        ctx.type = ctx.fatorArit().type
        ctx.val = ctx.fatorArit().val

    # Enter a parse tree produced by trabalhoFinalParser#MultDiv.
    def enterMultDiv(self, ctx: trabalhoFinalParser.MultDivContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#MultDiv.
    def exitMultDiv(self, ctx: trabalhoFinalParser.MultDivContext):
        if self.numeric_type(ctx.termoArit().type) and self.numeric_type(ctx.fatorArit().type):
            if ctx.termoArit().type == 'real' and ctx.fatorArit().type == 'real':
                ctx.type = 'real'
                v1, v2 = ctx.termoArit().val, ctx.fatorArit().val

            elif ctx.termoArit().type == 'int' and ctx.fatorArit().type == 'real':
                ctx.type = 'real'
                v1, v2 = float(ctx.termoArit().val), ctx.fatorArit().val

            elif ctx.termoArit().type == 'real' and ctx.fatorArit().type == 'int':
                ctx.type = 'real'
                v1, v2 = ctx.termoArit().val, float(ctx.fatorArit().val)
            else:
                ctx.type = 'int'
                v1, v2 = ctx.termoArit().val, ctx.fatorArit().val

            if ctx.op.text == '*':
                ctx.val = v1 * v2
            else:
                ctx.val = v1 / v2
        else:
            raise ExpressionTypeError(ctx.start.line, ctx.op.text, ctx.termoArit().type, ctx.fatorArit().type)

    # Enter a parse tree produced by trabalhoFinalParser#ExprAritParenteses.
    def enterExprAritParenteses(self, ctx: trabalhoFinalParser.ExprAritParentesesContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#ExprAritParenteses.
    def exitExprAritParenteses(self, ctx: trabalhoFinalParser.ExprAritParentesesContext):
        ctx.type = ctx.exprArit().type
        ctx.val = ctx.exprArit().val

    # Enter a parse tree produced by trabalhoFinalParser#MenosUnario.
    def enterMenosUnario(self, ctx: trabalhoFinalParser.MenosUnarioContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#MenosUnario.
    def exitMenosUnario(self, ctx: trabalhoFinalParser.MenosUnarioContext):
        if self.numeric_type(ctx.fatorArit().type):
            ctx.type = ctx.fatorArit().type
            ctx.val = - ctx.fatorArit().val
        else:
            raise ExpressionTypeError(ctx.start.line, '- unário', ctx.fatorArit().type, None)

    # Enter a parse tree produced by trabalhoFinalParser#Real.
    def enterReal(self, ctx: trabalhoFinalParser.RealContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#Real.
    def exitReal(self, ctx: trabalhoFinalParser.RealContext):
        ctx.type = 'real'
        ctx.val = float(ctx.REAL().getText())

    # Enter a parse tree produced by trabalhoFinalParser#Inteiro.
    def enterInteiro(self, ctx: trabalhoFinalParser.InteiroContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#Inteiro.
    def exitInteiro(self, ctx: trabalhoFinalParser.InteiroContext):
        ctx.type = 'int'
        ctx.val = int(ctx.INT().getText())

    # Enter a parse tree produced by trabalhoFinalParser#IdentificadorA.
    def enterIdentificadorA(self, ctx: trabalhoFinalParser.IdentificadorAContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#IdentificadorA.
    def exitIdentificadorA(self, ctx: trabalhoFinalParser.IdentificadorAContext):
        id_name = ctx.ID().getText()

        if id_name in self.symbolTableLocal:  # verifica se o identificador foi declarado localmente
            ctx.type = self.symbolTableLocal[id_name][0]
            ctx.val = self.symbolTableLocal[id_name][1]
        elif id_name in self.symbolTable:  # verifica de foi declarado globalmente
            ctx.type = self.symbolTable[id_name][0]
            ctx.val = self.symbolTable[id_name][1]
        else:
            raise UndeclaredVariable(ctx.start.line, id_name)  # gera erro de variável não declarada

    # Enter a parse tree produced by trabalhoFinalParser#ChamaFuncaoA.
    def enterChamaFuncaoA(self, ctx: trabalhoFinalParser.ChamaFuncaoAContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#ChamaFuncaoA.
    def exitChamaFuncaoA(self, ctx: trabalhoFinalParser.ChamaFuncaoAContext):
        ctx.type = ctx.callF().type
        ctx.val = ctx.callF().val

    # Enter a parse tree produced by trabalhoFinalParser#Expr_Rel2.
    def enterExpr_Rel2(self, ctx: trabalhoFinalParser.Expr_Rel2Context):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#Expr_Rel2.
    def exitExpr_Rel2(self, ctx: trabalhoFinalParser.Expr_Rel2Context):
        ctx.type = ctx.exprRel2().type
        ctx.val = ctx.exprRel2().val

    # Enter a parse tree produced by trabalhoFinalParser#OrLogic.
    def enterOrLogic(self, ctx: trabalhoFinalParser.OrLogicContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#OrLogic.
    def exitOrLogic(self, ctx: trabalhoFinalParser.OrLogicContext):
        if ctx.exprRel().type == 'boolean' and ctx.exprRel2().type == 'boolean':
            ctx.type = 'boolean'
            ctx.val = 'True' if ctx.exprRel().val or ctx.exprRel2().val else 'False'
        else:
            raise ExpressionTypeError(ctx.start.line, 'OR', ctx.exprRel().type, ctx.exprRel2().type)

    # Enter a parse tree produced by trabalhoFinalParser#Expr_Rel3.
    def enterExpr_Rel3(self, ctx: trabalhoFinalParser.Expr_Rel3Context):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#Expr_Rel3.
    def exitExpr_Rel3(self, ctx: trabalhoFinalParser.Expr_Rel3Context):
        ctx.type = ctx.exprRel3().type
        ctx.val = ctx.exprRel3().val

    # Enter a parse tree produced by trabalhoFinalParser#AndLogic.
    def enterAndLogic(self, ctx: trabalhoFinalParser.AndLogicContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#AndLogic.
    def exitAndLogic(self, ctx: trabalhoFinalParser.AndLogicContext):
        if ctx.exprRel2().type == 'boolean' and ctx.exprRel3().type == 'boolean':
            ctx.type = 'boolean'
            ctx.val = 'True' if ctx.exprRel2().val and ctx.exprRel3().val else 'False'
        else:
            raise ExpressionTypeError(ctx.start.line, 'AND', ctx.exprRel2().type, ctx.termoRel().type)

    # Enter a parse tree produced by trabalhoFinalParser#CompRel.
    def enterCompRel(self, ctx: trabalhoFinalParser.CompRelContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#CompRel.
    def exitCompRel(self, ctx: trabalhoFinalParser.CompRelContext):
        if ctx.exprRel3().type == 'String' and ctx.termoRel().type == 'String':
            ctx.type = 'boolean'
            if ctx.op.text == '>':
                ctx.val = 'True' if len(ctx.exprRel3().val) > len(ctx.termoRel().val) else 'False'
            elif ctx.op.text == '<':
                ctx.val = 'True' if len(ctx.exprRel3().val) < len(ctx.termoRel().val) else 'False'
            elif ctx.op.text == '>=':
                ctx.val = 'True' if len(ctx.exprRel3().val) >= len(ctx.termoRel().val) else 'False'
            elif ctx.op.text == '<=':
                ctx.val = 'True' if len(ctx.exprRel3().val) <= len(ctx.termoRel().val) else 'False'
        else:
            raise ExpressionTypeError(ctx.start.line, ctx.op.text, ctx.termoRel().type, ctx.fatorRel().type)

    # Enter a parse tree produced by trabalhoFinalParser#CompArit.
    def enterCompArit(self, ctx: trabalhoFinalParser.CompAritContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#CompArit.
    def exitCompArit(self, ctx: trabalhoFinalParser.CompAritContext):
        if self.numeric_type(ctx.a.type) and self.numeric_type(ctx.b.type):
            ctx.type = 'boolean'
            if ctx.op.text == '>':
                ctx.val = 'True' if ctx.a.val > ctx.b.val else 'False'
            elif ctx.op.text == '<':
                ctx.val = 'True' if ctx.a.val < ctx.b.val else 'False'
            elif ctx.op.text == '>=':
                ctx.val = 'True' if ctx.a.val >= ctx.b.val else 'False'
            elif ctx.op.text == '<=':
                ctx.val = 'True' if ctx.a.val <= ctx.b.val else 'False'
        else:
            raise ExpressionTypeError(ctx.start.line, ctx.op.text, ctx.a.type, ctx.b.type)

    # Enter a parse tree produced by trabalhoFinalParser#Termo_Rel.
    def enterTermo_Rel(self, ctx: trabalhoFinalParser.Termo_RelContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#Termo_Rel.
    def exitTermo_Rel(self, ctx: trabalhoFinalParser.Termo_RelContext):
        ctx.type = ctx.termoRel().type
        ctx.val = ctx.termoRel().val

    # Enter a parse tree produced by trabalhoFinalParser#EqRel.
    def enterEqRel(self, ctx: trabalhoFinalParser.EqRelContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#EqRel.
    def exitEqRel(self, ctx: trabalhoFinalParser.EqRelContext):
        if (ctx.termoRel().type == 'boolean' and ctx.fatorRel().type == 'boolean') or \
                (ctx.termoRel().type == 'String' and ctx.fatorRel().type == 'String'):
            ctx.type = 'boolean'
            if ctx.op.text == '==':
                ctx.val = 'True' if ctx.termoRel().val == ctx.fatorRel().val else 'False'
            elif ctx.op.text == '!=':
                ctx.val = 'False' if ctx.termoRel().val == ctx.fatorRel().val else 'True'
        else:
            raise ExpressionTypeError(ctx.start.line, ctx.op.text, ctx.superExprRel().type, ctx.exprRel().type)

    # Enter a parse tree produced by trabalhoFinalParser#EqArit.
    def enterEqArit(self, ctx: trabalhoFinalParser.EqAritContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#EqArit.
    def exitEqArit(self, ctx: trabalhoFinalParser.EqAritContext):
        if self.numeric_type(ctx.a.type) and self.numeric_type(ctx.b.type):
            ctx.type = 'boolean'
            if ctx.op.text == '==':
                ctx.val = 'True' if ctx.a.val == ctx.b.val else 'False'
            elif ctx.op.text == '!=':
                ctx.val = 'False' if ctx.a.val == ctx.b.val else 'True'

    # Enter a parse tree produced by trabalhoFinalParser#Fator_Rel.
    def enterFator_Rel(self, ctx: trabalhoFinalParser.Fator_RelContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#Fator_Rel.
    def exitFator_Rel(self, ctx: trabalhoFinalParser.Fator_RelContext):
        ctx.type = ctx.fatorRel().type
        ctx.val = ctx.fatorRel().val

    # Enter a parse tree produced by trabalhoFinalParser#ExprRelParenteses.
    def enterExprRelParenteses(self, ctx: trabalhoFinalParser.ExprRelParentesesContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#ExprRelParenteses.
    def exitExprRelParenteses(self, ctx: trabalhoFinalParser.ExprRelParentesesContext):
        ctx.type = ctx.exprRel().type
        ctx.val = ctx.exprRel().val

    # Enter a parse tree produced by trabalhoFinalParser#Not.
    def enterNot(self, ctx: trabalhoFinalParser.NotContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#Not.
    def exitNot(self, ctx: trabalhoFinalParser.NotContext):
        if ctx.fatorRel().type == 'boolean':
            ctx.type = 'boolean'
            ctx.val = not ctx.fatorRel().val
        else:
            raise ExpressionTypeError(ctx.start.line, '! (not)', ctx.termoRel().type, None)

    # Enter a parse tree produced by trabalhoFinalParser#Booleano.
    def enterBooleano(self, ctx: trabalhoFinalParser.BooleanoContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#Booleano.
    def exitBooleano(self, ctx: trabalhoFinalParser.BooleanoContext):
        ctx.type = 'boolean'
        ctx.val = ctx.BOOL().getText()

    # Enter a parse tree produced by trabalhoFinalParser#String.
    def enterString(self, ctx: trabalhoFinalParser.StringContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#String.
    def exitString(self, ctx: trabalhoFinalParser.StringContext):
        ctx.type = 'String'
        ctx.val = ctx.STR().getText()

    # Enter a parse tree produced by trabalhoFinalParser#IdentificadorR.
    def enterIdentificadorR(self, ctx: trabalhoFinalParser.IdentificadorRContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#IdentificadorR.
    def exitIdentificadorR(self, ctx: trabalhoFinalParser.IdentificadorRContext):
        id_name = ctx.ID().getText()

        if id_name in self.symbolTableLocal:  # verifica se o identificador foi declarado localmente
            ctx.type = self.symbolTableLocal[id_name][0]
            ctx.val = self.symbolTableLocal[id_name][1]
        elif id_name in self.symbolTable:  # verifica de foi declarado globalmente
            ctx.type = self.symbolTable[id_name][0]
            ctx.val = self.symbolTable[id_name][1]
        else:
            raise UndeclaredVariable(ctx.start.line, id_name)  # gera erro de variável não declarada

    # Enter a parse tree produced by trabalhoFinalParser#ChamaFuncaoR.
    def enterChamaFuncaoR(self, ctx: trabalhoFinalParser.ChamaFuncaoRContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#ChamaFuncaoR.
    def exitChamaFuncaoR(self, ctx: trabalhoFinalParser.ChamaFuncaoRContext):
        ctx.type = ctx.callF().type
        ctx.val = ctx.callF().val

    # Enter a parse tree produced by trabalhoFinalParser#atribuicao.
    def enterAtribuicao(self, ctx: trabalhoFinalParser.AtribuicaoContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#atribuicao.
    def exitAtribuicao(self, ctx: trabalhoFinalParser.AtribuicaoContext):
        id_name = ctx.ID().getText()

        if id_name in self.symbolTableLocal:
            esperado = self.symbolTableLocal[id_name][0]  # tipo esperaddo
            recebido = ctx.expr().type  # tipo recebido
            if esperado != recebido:
                raise UnexpectedTypeError(ctx.start.line, esperado, recebido)
            else:
                self.symbolTableLocal[id_name][1] = ctx.expr().val
        elif id_name in self.symbolTable:
            esperado = self.symbolTable[id_name][0]  # tipo esperaddo
            recebido = ctx.expr().type  # tipo recebido
            if esperado != recebido:
                raise UnexpectedTypeError(ctx.start.line, esperado, recebido)
            else:
                self.symbolTable[id_name][1] = ctx.expr().val
        else:
            raise UndeclaredVariable(ctx.start.line, id_name)

    # Enter a parse tree produced by trabalhoFinalParser#print.
    def enterPrint(self, ctx: trabalhoFinalParser.PrintContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#print.
    def exitPrint(self, ctx: trabalhoFinalParser.PrintContext):
        listaexpr = ''
        for expr in ctx.expr():
            if expr.type == 'String' and '"' in expr.val:
                val = expr.val
                expr.val = val.replace('"', '')  # retira as aspas duplas da string
            listaexpr += str(expr.val)
        print(listaexpr)

    # Enter a parse tree produced by trabalhoFinalParser#input.
    def enterInput(self, ctx: trabalhoFinalParser.InputContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#input.
    def exitInput(self, ctx: trabalhoFinalParser.InputContext):
        strlistaIds = ctx.listaIdsPrint().getText()
        id_names = strlistaIds.split(',')

        for id_name in id_names:
            if id_name not in self.symbolTable and id_name not in self.symbolTableLocal:
                raise UndeclaredVariable(ctx.start.line, id_name)

    # Enter a parse tree produced by trabalhoFinalParser#listaIdsPrint.
    def enterListaIdsPrint(self, ctx: trabalhoFinalParser.ListaIdsPrintContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#listaIdsPrint.
    def exitListaIdsPrint(self, ctx: trabalhoFinalParser.ListaIdsPrintContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#if.
    def enterIf(self, ctx: trabalhoFinalParser.IfContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#if.
    def exitIf(self, ctx: trabalhoFinalParser.IfContext):
        if ctx.exprRel().type != 'boolean':
            raise UnexpectedTypeError(ctx.start.line, 'boolean', ctx.exprRel().type)

    # Enter a parse tree produced by trabalhoFinalParser#ifRep.
    def enterIfRep(self, ctx: trabalhoFinalParser.IfRepContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#ifRep.
    def exitIfRep(self, ctx: trabalhoFinalParser.IfRepContext):
        if ctx.exprRel().type != 'boolean':
            raise UnexpectedTypeError(ctx.start.line, 'boolean', ctx.exprRel().type)

    # Enter a parse tree produced by trabalhoFinalParser#else.
    def enterElse(self, ctx: trabalhoFinalParser.ElseContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#else.
    def exitElse(self, ctx: trabalhoFinalParser.ElseContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#elseRep.
    def enterElseRep(self, ctx: trabalhoFinalParser.ElseRepContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#elseRep.
    def exitElseRep(self, ctx: trabalhoFinalParser.ElseRepContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#for.
    def enterFor(self, ctx: trabalhoFinalParser.ForContext):
        atrib = ctx.atribFor().getText()
        lista = atrib.split('=')
        ctx_id = lista[0]

        if ctx_id in self.symbolTableLocal:
            if not self.numeric_type(self.symbolTableLocal[ctx_id][0]):
                raise UnexpectedTypeError(ctx.start.line, 'int', self.symbolTableLocal[ctx_id][0])
        elif ctx_id in self.symbolTable:
            if not self.numeric_type(self.symbolTable[ctx_id][0]):
                raise UnexpectedTypeError(ctx.start.line, 'int', self.symbolTable[ctx_id][0])
        else:
            raise UndeclaredVariable(ctx.start.line, ctx_id)

        self.stack.append('loop')

    # Exit a parse tree produced by trabalhoFinalParser#for.
    def exitFor(self, ctx: trabalhoFinalParser.ForContext):
        self.stack.pop()

    # Enter a parse tree produced by trabalhoFinalParser#atribFor.
    def enterAtribFor(self, ctx: trabalhoFinalParser.AtribForContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#atribFor.
    def exitAtribFor(self, ctx: trabalhoFinalParser.AtribForContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#incdec.
    def enterIncdec(self, ctx: trabalhoFinalParser.IncdecContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#incdec.
    def exitIncdec(self, ctx: trabalhoFinalParser.IncdecContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#break.
    def enterBreak(self, ctx: trabalhoFinalParser.BreakContext):
        if 'loop' not in self.stack:
            raise UnexpectedBreak(ctx.start.line)

    # Exit a parse tree produced by trabalhoFinalParser#break.
    def exitBreak(self, ctx: trabalhoFinalParser.BreakContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#while.
    def enterWhile(self, ctx: trabalhoFinalParser.WhileContext):
        self.stack.append('loop')

    # Exit a parse tree produced by trabalhoFinalParser#while.
    def exitWhile(self, ctx: trabalhoFinalParser.WhileContext):
        if ctx.exprRel().type != 'boolean':
            raise UnexpectedTypeError(ctx.start.line, 'boolean', ctx.exprRel().type)
        self.stack.pop()

    # Enter a parse tree produced by trabalhoFinalParser#return.
    def enterReturn(self, ctx: trabalhoFinalParser.ReturnContext):
        if not self._active_function():  # se não há uma função ativa
            raise UnexpectedReturn(ctx.start.line)

    # Exit a parse tree produced by trabalhoFinalParser#return.
    def exitReturn(self, ctx: trabalhoFinalParser.ReturnContext):
        tipoEsperado = self.symbolTable[self.active_function[-1]][0]
        if ctx.expr():
            if ctx.expr().type != tipoEsperado:
                raise UnexpectedReturnTypeError(ctx.start.line, tipoEsperado, ctx.expr().type)
        ctx.retorno = ctx.expr().val
        self.symbolTable[self.active_function[-1]][1] = ctx.retorno


del trabalhoFinalParser
