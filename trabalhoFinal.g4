grammar trabalhoFinal;

prog: decVarConst* decFunc* main
    ;

decVarConst: decVar
    | 'const' tipo listaAtrib ';'
    ;

decVar: tipo listaIds ';';

tipo: 'int'
    | 'real'
    | 'boolean'
    | 'String'
    ;

listaIds: ID (',' ID)*
    ;

listaAtrib: atrib (',' atrib)*
    ;

atrib: ID '=' valor
    ;

valor returns [type]
    : '-'? INT #ValorInteiro
    | '-'? REAL #ValorReal
    | STR #ValorString
    | BOOL #ValorBool
    ;

// Declaração de função
decFunc: tipoFun ID '(' listaParams ')' '{' decVar* comandos '}'
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
main: 'main' '(' ')' '{' decVar* comandos '}'
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
    : '(' expr ')' #ExprParenteses
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
    | '!' exprRel #Not
    | BOOL #Booleano
    | STR #String
    | ID #IdentificadorR
    | callF #ChamaFuncaoR
    ;

atribuicao: ID '=' expr ';';

// Funções nativas
print: 'print' '(' expr (',' expr)* ')' ';';

input: 'input' '(' listaIds ')' ';';

if: 'if' '(' exprRel ')' '{' comandos '}' else? ;

// if dentro de um comando de repetição
ifRep: 'if' '(' exprRel ')' '{' comandosRep '}' elseRep? ;

else: 'else' '{' comandos '}';

// else dentro de um comando de repetição
elseRep: 'else' '{' comandosRep '}';

// Comandos de repetição
for: 'for' '(' listaAtribFor ';' exprRel ';' incdec ')' '{' comandosRep '}';

listaAtribFor: atribFor (',' atribFor)*;

atribFor: ID '=' valorFor
    ;

valorFor returns [type]
    : '-'? INT #ValorInteiroFor
    | '-'? REAL #ValorRealFor
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
REAL: [0-9]+('.'[0-9]+)?; // interrogação quer dizer que é opcional
INT: [0-9]+;
STR: '"' .*? '"'; // o ponto casa com qualquer caractere único
BOOL: 'True' | 'False';
ID: [a-zA-Z][a-zA-Z0-9]*;
WS: [ \t\r\n]+ -> skip;