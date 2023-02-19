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
    | exprBool  #Expr_Bool
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

exprBool returns [type]
    : exprBool '||' exprBool2 #OrLogic
    | exprBool2 #Expr_Bool2
    ;

exprBool2 returns [type]
    : exprBool2 '&&' exprBool3 #AndLogic
    | exprBool3 #Expr_Bool3
    ;

exprBool3 returns [type]
    : a=exprArit op=('>='|'<='|'>'|'<') b=exprArit #CompArit
    | exprBool3  op=('>='|'<='|'>'|'<') termoBool #CompBool
    | termoBool #Termo_Bool
    ;

termoBool returns [type]
    : a=exprArit op=('=='|'!=') b=exprArit #EqArit
    | termoBool  op=('=='|'!=') fatorBool #EqBool
    | fatorBool #Fator_Bool
    ;

fatorBool returns [type]
    : '(' exprBool ')' #ExprBoolParenteses
    | '!' exprBool #Not
    | BOOL #Booleano
    | STR #String
    | ID #IdentificadorB
    | callF #ChamaFuncaoB
    ;

atribuicao: ID '=' expr ';';

// Funções nativas
print: 'print' '(' expr (',' expr)* ')' ';';

input: 'input' '(' listaIds ')' ';';

if: 'if' '(' exprBool ')' '{' comandos '}' else? ;

// if dentro de um comando de repetição
ifRep: 'if' '(' exprBool ')' '{' comandosRep '}' elseRep? ;

else: 'else' '{' comandos '}';

// else dentro de um comando de repetição
elseRep: 'else' '{' comandosRep '}';

// Comandos de repetição
for: 'for' '(' listaAtribFor ';' exprBool ';' incdec ')' '{' comandosRep '}';

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

while: 'while' '(' exprBool ')' '{' comandosRep '}'
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