from antlr4 import *
from gen.trabalhoFinalParser import trabalhoFinalParser
from gen.trabalhoFinalListener import trabalhoFinalListener


# Definicao da classe MyListener
class trabalhoFinalMyListener(trabalhoFinalListener):
    symbolTable = {}  # ESTRUTURA DA TS {(ID, ESCOPO) : [TIPO, VALOR_CONSTANTE]}  ESCOPO = 0 (GLOGAL) ESCOPO = 1 (LOCAL)
    f_args = {}
    stack = []
    active_functions = []
    reserved = ["'True'", "'False'", "'if'", "'else'", "'for'", "'while'", "'print'", "'input'", "'int'",
                "'real'", "'String'", "'boolean'", "'main'", "'return'", "'break'", "'const'"]

    def numeric_type(self, vtype):  # função que verifica se é um tipo numério
        return (vtype == 'int') or (vtype == 'real')

    def active_function(self):
        return 'function' in self.stack

    # Enter a parse tree produced by projetoFinalParser#prog.
    def enterProg(self, ctx: trabalhoFinalParser.ProgContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#prog.
    def exitProg(self, ctx: trabalhoFinalParser.ProgContext):
        print(self.symbolTable)

    # Enter a parse tree produced by trabalhoFinalParser#decConst.
    def enterDecConst(self, ctx: trabalhoFinalParser.DecConstContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#decConst.
    def exitDecConst(self, ctx: trabalhoFinalParser.DecConstContext):
        variaveis = ctx.listaAtrib().listaids
        tipos = ctx.listaAtrib().listatipos

        for var in variaveis:
            self.symbolTable[(var, 0)][0] = ctx.tipo().getText()
            if self.symbolTable[(var, 0)][1] in self.reserved:
                print("Reserverd error.")

        for i in range(len(variaveis)):
            if ctx.tipo().getText() != tipos[i]:
                print("Erro: O tipo da variável não é compatível com o seu valor.")

        for var in variaveis:
            if ctx.tipo().getText() == 'int':
                self.symbolTable[(var, 0)][1] = int(self.symbolTable[(var, 0)][1])
            elif ctx.tipo().getText() == 'real':
                self.symbolTable[(var, 0)][1] = float(self.symbolTable[(var, 0)][1])

    # Enter a parse tree produced by trabalhoFinalParser#decVar.
    def enterDecVar(self, ctx: trabalhoFinalParser.DecVarContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#decVar.
    def exitDecVar(self, ctx: trabalhoFinalParser.DecVarContext):
        variaveis = ctx.listaIds().lista

        # valor padrão das variáveis
        for var in variaveis:
            self.symbolTable[(var, 0)][0] = ctx.tipo().getText()
            if ctx.tipo().getText() == 'String':
                self.symbolTable[(var, 0)][1] = "''"
            elif self.numeric_type(ctx.tipo().getText()):
                self.symbolTable[(var, 0)][1] = 0
            elif ctx.tipo().getText() == 'boolean':
                self.symbolTable[var][1] = 'False'

    # Enter a parse tree produced by trabalhoFinalParser#listaIds.
    def enterListaIds(self, ctx: trabalhoFinalParser.ListaIdsContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#listaIds.
    def exitListaIds(self, ctx: trabalhoFinalParser.ListaIdsContext):
        ids = []
        for token in ctx.ID():
            if token.getText() in self.reserved:
                print("Erro: palavra reservada não pode ser usada como nome de variável.")
            if (token.getText(), 0) in self.symbolTable:
                print('Erro: variável com mesmo nome já declarada.')
            ids.append(token.getText())
        for i in range(len(ids)):
            self.symbolTable[(ctx.ID(i).getText(), 0)] = [None, None]
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
            valores.append(valor.getText())  # lista de valores
            tipos.append(valor.type)  # lista de tipos
        for token in ctx.ID():
            if (token.getText(), 0) in self.symbolTable:
                print('Erro: variável com mesmo nome já declarada.')
            if (token.getText(), 0) in self.reserved:
                print('Erro: palavra reservada não pode ser usada como nome de variável.')
            ids.append(token.getText())
        for i in range(len(ids)):
            self.symbolTable[(ctx.ID(i).getText(), 0)] = [None, valores[i]]
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
            ctx.val = - float(ctx.REAL().getText())
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

    # Enter a parse tree produced by trabalhoFinalParser#decFunc.
    def enterDecFunc(self, ctx: trabalhoFinalParser.DecFuncContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#decFunc.
    def exitDecFunc(self, ctx: trabalhoFinalParser.DecFuncContext):
        pass

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
        pass

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
        pass

    # Exit a parse tree produced by trabalhoFinalParser#callF.
    def exitCallF(self, ctx: trabalhoFinalParser.CallFContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#Expr_Arit.
    def enterExpr_Arit(self, ctx: trabalhoFinalParser.Expr_AritContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#Expr_Arit.
    def exitExpr_Arit(self, ctx: trabalhoFinalParser.Expr_AritContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#Expr_Bool.
    def enterExpr_Rel(self, ctx: trabalhoFinalParser.Expr_RelContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#Expr_Bool.
    def exitExpr_Rel(self, ctx: trabalhoFinalParser.Expr_RelContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#Termo_Arit.
    def enterTermo_Arit(self, ctx: trabalhoFinalParser.Termo_AritContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#Termo_Arit.
    def exitTermo_Arit(self, ctx: trabalhoFinalParser.Termo_AritContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#SomaSub.
    def enterSomaSub(self, ctx: trabalhoFinalParser.SomaSubContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#SomaSub.
    def exitSomaSub(self, ctx: trabalhoFinalParser.SomaSubContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#Fator_Arit.
    def enterFator_Arit(self, ctx: trabalhoFinalParser.Fator_AritContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#Fator_Arit.
    def exitFator_Arit(self, ctx: trabalhoFinalParser.Fator_AritContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#MultDiv.
    def enterMultDiv(self, ctx: trabalhoFinalParser.MultDivContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#MultDiv.
    def exitMultDiv(self, ctx: trabalhoFinalParser.MultDivContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#ExprParenteses.
    def enterExprParenteses(self, ctx: trabalhoFinalParser.ExprParentesesContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#ExprParenteses.
    def exitExprParenteses(self, ctx: trabalhoFinalParser.ExprParentesesContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#MenosUnario.
    def enterMenosUnario(self, ctx: trabalhoFinalParser.MenosUnarioContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#MenosUnario.
    def exitMenosUnario(self, ctx: trabalhoFinalParser.MenosUnarioContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#Real.
    def enterReal(self, ctx: trabalhoFinalParser.RealContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#Real.
    def exitReal(self, ctx: trabalhoFinalParser.RealContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#Inteiro.
    def enterInteiro(self, ctx: trabalhoFinalParser.InteiroContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#Inteiro.
    def exitInteiro(self, ctx: trabalhoFinalParser.InteiroContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#IdentificadorA.
    def enterIdentificadorA(self, ctx: trabalhoFinalParser.IdentificadorAContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#IdentificadorA.
    def exitIdentificadorA(self, ctx: trabalhoFinalParser.IdentificadorAContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#ChamaFuncaoA.
    def enterChamaFuncaoA(self, ctx: trabalhoFinalParser.ChamaFuncaoAContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#ChamaFuncaoA.
    def exitChamaFuncaoA(self, ctx: trabalhoFinalParser.ChamaFuncaoAContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#Expr_Rel2.
    def enterExpr_Rel2(self, ctx: trabalhoFinalParser.Expr_Rel2Context):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#Expr_Rel2.
    def exitExpr_Rel2(self, ctx: trabalhoFinalParser.Expr_Rel2Context):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#OrLogic.
    def enterOrLogic(self, ctx: trabalhoFinalParser.OrLogicContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#OrLogic.
    def exitOrLogic(self, ctx: trabalhoFinalParser.OrLogicContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#Expr_Rel3.
    def enterExpr_Rel3(self, ctx: trabalhoFinalParser.Expr_Rel3Context):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#Expr_Rel3.
    def exitExpr_Rel3(self, ctx: trabalhoFinalParser.Expr_Rel3Context):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#AndLogic.
    def enterAndLogic(self, ctx: trabalhoFinalParser.AndLogicContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#AndLogic.
    def exitAndLogic(self, ctx: trabalhoFinalParser.AndLogicContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#CompRel.
    def enterCompRel(self, ctx: trabalhoFinalParser.CompRelContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#CompRel.
    def exitCompRel(self, ctx: trabalhoFinalParser.CompRelContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#CompArit.
    def enterCompArit(self, ctx: trabalhoFinalParser.CompAritContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#CompArit.
    def exitCompArit(self, ctx: trabalhoFinalParser.CompAritContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#Termo_Rel.
    def enterTermo_Rel(self, ctx: trabalhoFinalParser.Termo_RelContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#Termo_Rel.
    def exitTermo_Rel(self, ctx: trabalhoFinalParser.Termo_RelContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#EqRel.
    def enterEqRel(self, ctx: trabalhoFinalParser.EqRelContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#EqRel.
    def exitEqRel(self, ctx: trabalhoFinalParser.EqRelContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#EqArit.
    def enterEqArit(self, ctx: trabalhoFinalParser.EqAritContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#EqArit.
    def exitEqArit(self, ctx: trabalhoFinalParser.EqAritContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#Fator_Rel.
    def enterFator_Rel(self, ctx: trabalhoFinalParser.Fator_RelContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#Fator_Rel.
    def exitFator_Rel(self, ctx: trabalhoFinalParser.Fator_RelContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#ExprRelParenteses.
    def enterExprRelParenteses(self, ctx: trabalhoFinalParser.ExprRelParentesesContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#ExprRelParenteses.
    def exitExprRelParenteses(self, ctx: trabalhoFinalParser.ExprRelParentesesContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#Not.
    def enterNot(self, ctx: trabalhoFinalParser.NotContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#Not.
    def exitNot(self, ctx: trabalhoFinalParser.NotContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#Booleano.
    def enterBooleano(self, ctx: trabalhoFinalParser.BooleanoContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#Booleano.
    def exitBooleano(self, ctx: trabalhoFinalParser.BooleanoContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#String.
    def enterString(self, ctx: trabalhoFinalParser.StringContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#String.
    def exitString(self, ctx: trabalhoFinalParser.StringContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#IdentificadorR.
    def enterIdentificadorR(self, ctx: trabalhoFinalParser.IdentificadorRContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#IdentificadorR.
    def exitIdentificadorR(self, ctx: trabalhoFinalParser.IdentificadorRContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#ChamaFuncaoR.
    def enterChamaFuncaoR(self, ctx: trabalhoFinalParser.ChamaFuncaoRContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#ChamaFuncaoR.
    def exitChamaFuncaoR(self, ctx: trabalhoFinalParser.ChamaFuncaoRContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#atribuicao.
    def enterAtribuicao(self, ctx: trabalhoFinalParser.AtribuicaoContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#atribuicao.
    def exitAtribuicao(self, ctx: trabalhoFinalParser.AtribuicaoContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#print.
    def enterPrint(self, ctx: trabalhoFinalParser.PrintContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#print.
    def exitPrint(self, ctx: trabalhoFinalParser.PrintContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#input.
    def enterInput(self, ctx: trabalhoFinalParser.InputContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#input.
    def exitInput(self, ctx: trabalhoFinalParser.InputContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#if.
    def enterIf(self, ctx: trabalhoFinalParser.IfContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#if.
    def exitIf(self, ctx: trabalhoFinalParser.IfContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#ifRep.
    def enterIfRep(self, ctx: trabalhoFinalParser.IfRepContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#ifRep.
    def exitIfRep(self, ctx: trabalhoFinalParser.IfRepContext):
        pass

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
        pass

    # Exit a parse tree produced by trabalhoFinalParser#for.
    def exitFor(self, ctx: trabalhoFinalParser.ForContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#listaAtribFor.
    def enterListaAtribFor(self, ctx: trabalhoFinalParser.ListaAtribForContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#listaAtribFor.
    def exitListaAtribFor(self, ctx: trabalhoFinalParser.ListaAtribForContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#atribFor.
    def enterAtribFor(self, ctx: trabalhoFinalParser.AtribForContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#atribFor.
    def exitAtribFor(self, ctx: trabalhoFinalParser.AtribForContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#ValorInteiroFor.
    def enterValorInteiroFor(self, ctx: trabalhoFinalParser.ValorInteiroForContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#ValorInteiroFor.
    def exitValorInteiroFor(self, ctx: trabalhoFinalParser.ValorInteiroForContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#ValorRealFor.
    def enterValorRealFor(self, ctx: trabalhoFinalParser.ValorRealForContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#ValorRealFor.
    def exitValorRealFor(self, ctx: trabalhoFinalParser.ValorRealForContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#incdec.
    def enterIncdec(self, ctx: trabalhoFinalParser.IncdecContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#incdec.
    def exitIncdec(self, ctx: trabalhoFinalParser.IncdecContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#break.
    def enterBreak(self, ctx: trabalhoFinalParser.BreakContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#break.
    def exitBreak(self, ctx: trabalhoFinalParser.BreakContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#while.
    def enterWhile(self, ctx: trabalhoFinalParser.WhileContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#while.
    def exitWhile(self, ctx: trabalhoFinalParser.WhileContext):
        pass

    # Enter a parse tree produced by trabalhoFinalParser#return.
    def enterReturn(self, ctx: trabalhoFinalParser.ReturnContext):
        pass

    # Exit a parse tree produced by trabalhoFinalParser#return.
    def exitReturn(self, ctx: trabalhoFinalParser.ReturnContext):
        pass


del trabalhoFinalParser
