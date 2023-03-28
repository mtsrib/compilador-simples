grammar trabalhoFinal;

prog: decVarConst* decFunc* main
    ;

decVarConst: decVar
    | decConst
    ;

decConst: 'const' tipo listaAtrib ';';

decVar: tipo listaIds ';';

tipo: 'int'
    | 'real'
    | 'boolean'
    | 'String'
    ;

listaIds returns [lista[]]
    : ID (',' ID)*
    ;

listaAtrib returns [listaids[], listatipos[]]
    : ID '=' valor (',' ID '=' valor)*
    ;

valor returns [type]
    : '-'? INT #ValorInteiro
    | '-'? REAL #ValorReal
    | STR #ValorString
    | BOOL #ValorBool
    ;

// Declaração de função
decFunc: tipoFun ID '(' listaParams ')' '{' decVarLocal* comandos '}' #Func_Type
    ;

decVarLocal: tipo listaIdsLocal ';';

listaIdsLocal returns [lista[]]
    : ID (',' ID)*
    ;

tipoFun: 'int'
    | 'real'
    | 'boolean'
    | 'String'
    |
    ;

listaParams: tipo ID (',' tipo ID)*
    |
    ;

// Função principal
main: 'main' '(' ')' '{' decVarLocal* comandos '}'
    ;

comandos: callF ';' comandos
    | atribuicao comandos
    | print comandos
    | input comandos
    | if comandos
    | for comandos
    | while comandos
    | return
    |
    ;

comandosRep: callF ';' comandosRep
    | atribuicao comandosRep
    | print comandosRep
    | input comandosRep
    | ifRep comandosRep
    | for comandosRep
    | while comandosRep
    | break comandosRep
    | return
    |
    ;


// Chamada de função
callF returns [type]
    : ID '(' expr (',' expr)* ')';

// Expressões artimeticas e booleanas
expr returns [type]
    : exprArit #Expr_Arit
    | exprRel  #Expr_Rel
    ;

exprArit returns [type]
    : exprArit op=('+'|'-') termoArit #SomaSub
    | termoArit #Termo_Arit
    ;

termoArit returns [type]
    : termoArit op=('*'|'/') fatorArit #MultDiv
    | fatorArit #Fator_Arit
    ;

fatorArit returns [type]
    : '(' exprArit ')' #ExprAritParenteses
    | '-' fatorArit #MenosUnario
    | REAL #Real
    | INT #Inteiro
    | ID #IdentificadorA
    | callF #ChamaFuncaoA
    ;

exprRel returns [type]
    : exprRel '||' exprRel2 #OrLogic
    | exprRel2 #Expr_Rel2
    ;

exprRel2 returns [type]
    : exprRel2 '&&' exprRel3 #AndLogic
    | exprRel3 #Expr_Rel3
    ;

exprRel3 returns [type]
    : a=exprArit op=('>='|'<='|'>'|'<') b=exprArit #CompArit
    | exprRel3  op=('>='|'<='|'>'|'<') termoRel #CompRel
    | termoRel #Termo_Rel
    ;

termoRel returns [type]
    : a=exprArit op=('=='|'!=') b=exprArit #EqArit
    | termoRel  op=('=='|'!=') fatorRel #EqRel
    | fatorRel #Fator_Rel
    ;

fatorRel returns [type]
    : '(' exprRel ')' #ExprRelParenteses
    | '!' fatorRel #Not
    | BOOL #Booleano
    | STR #String
    | ID #IdentificadorR
    | callF #ChamaFuncaoR
    ;

atribuicao: ID '=' expr ';';

// Funções nativas
print: 'print' '(' expr (',' expr)* ')' ';';

input: 'input' '(' listaIdsPrint ')' ';';

listaIdsPrint: ID (',' ID)*
    ;

if: 'if' '(' exprRel ')' '{' comandos '}' else? ;

// if dentro de um comando de repetição
ifRep: 'if' '(' exprRel ')' '{' comandosRep '}' elseRep? ;

else: 'else' '{' comandos '}';

// else dentro de um comando de repetição
elseRep: 'else' '{' comandosRep '}';

// Comandos de repetição
for: 'for' '(' atribFor ';' exprRel ';' incdec ')' '{' comandosRep '}';

atribFor: ID '=' valor
    ;

incdec: ID '=' ID op=('-'|'+') INT
    | ID '=' ID op=('-'|'+') REAL
;

break: 'break' ';'
    ;

while: 'while' '(' exprRel ')' '{' comandosRep '}'
    ;

return returns [retorno]
    : 'return' expr ';'
    ;

// Regras lexicas
INT: [0-9]+;
REAL: [0-9]+('.'[0-9]+)?; // interrogação quer dizer que é opcional
STR: '"' .*? '"'; // o ponto casa com qualquer caractere único
BOOL: 'True' | 'False';
ID: [a-zA-Z][a-zA-Z0-9]*;
WS: [ \t\r\n]+ -> skip;