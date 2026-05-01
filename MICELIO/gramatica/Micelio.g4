grammar Micelio; 

program : sep* (statement sep*)* EOF ;

statement
    : simple_stmt
    | compound_stmt
    ;

simple_stmt
    : var_decl
    | const_decl
    | assignment
    | return_stmt
    | break_stmt
    | continue_stmt
    | import_stmt
    | leer_stmt
    | imp_stmt
    | expr
    ;

compound_stmt
    : if_stmt
    | switch_stmt
    | while_stmt
    | for_stmt
    | func_def
    | block
    ;

var_decl : VAR ID (',' ID)* ('=' expr (',' expr)*)? ;
const_decl : CONST ID '=' expr ;
assignment : assign_target '=' expr ;
assign_target : ID ('[' expr ']')* ;
return_stmt : REGRESA expr? ;
break_stmt : ROMPER ;
continue_stmt : CONTINUAR ;
import_stmt : IMPORTAR STRING (COMO ID)? ;
leer_stmt : LEER ID ;
imp_stmt : IMP expr ;

if_stmt : SI '(' expr ')' sep* block (sep* SINO sep* block)? ;
switch_stmt : SEGUN '(' expr ')' sep* '{' sep* case_block+ '}' ;
case_block
    : CASO expr ':' sep* (statement sep*)*              #caseClause
    | DEFECTO ':' sep* (statement sep*)*                #defaultClause
    ;
while_stmt : MIENTRAS '(' expr ')' sep* block ;
for_stmt
    : PARA ID '=' expr HASTA expr (INC expr)? sep* block
    | PARA ID EN expr sep* block
    ;

func_def : FUNCION ID '(' param_list? ')' sep* block ;
param_list : param_item (',' param_item)* ;
param_item
    : ID                    # paramNormal
    | MUL ID                # paramArgs
    | POW ID                # paramKwargs
    ;

block : '{' sep* (statement sep*)* '}' ;

expr
    : postfixExpr                                                     #postfixRoot
    | op=(INC_OP | DEC_OP) expr                                       #preIncDec
    | expr op=(INC_OP | DEC_OP)                                       #postIncDec
    | '-' expr                                                        #unaryMinus
    | NO expr                                                         #notExpr
    | expr op=(MUL | DIV | MOD | DOTMUL) expr                        #mulDivMod
    | expr op=(PLUS | MINUS) expr                                     #addSub
    | expr op=POW expr                                                #powExpr
    | expr op=(EQ | NE | LT | LE | GT | GE) expr                      #comparison
    | expr Y expr                                                     #andExpr
    | expr O expr                                                     #orExpr
    | expr IN expr                                                    #inExpr
    | expr NEWLINE* PIPE NEWLINE* expr                                #pipeExpr
    ;

postfixExpr
    : primary postfixSuffix*                                          #postfixExprNode
    ;

primary
    : literal                                                         #literalExpr
    | ID                                                              #idExpr
    | '(' expr ')'                                                    #parenExpr
    | '[' (expr (',' expr)*)? ']'                                     #listExpr
    | SET '(' (expr (',' expr)*)? ')'                                 #setExpr
    | DICT '(' (keyValue (',' keyValue)*)? ')'                        #dictExpr
    | '{' (keyValue (',' keyValue)*)? '}'                             #mapLiteral
    | FUNCION '(' param_list? ')' block                               #anonFuncExpr
    | MATRIZ '(' expr ')'                                             #matrizExpr
    ;

postfixSuffix
    : '[' expr ']'                                                    #indexSuffix
    | '(' exprList? ')'                                               #callSuffix
    | '.' ID                                                          #memberSuffix
    ;

keyValue : expr ':' expr ;
exprList : expr (',' expr)* ;

literal : NUMBER | STRING | BOOL | NULL ;

sep : ';' | NEWLINE+ ;

VAR : 'var' ;
CONST : 'const' ;
FUNCION : 'funcion' ;
MATRIZ : 'matriz' ;
REGRESA : 'regresa' ;
SI : 'si' ;
SINO : 'sino' ;
SEGUN : 'segun' ;
CASO : 'caso' ;
DEFECTO : 'defecto' ;
PARA : 'para' ;
HASTA : 'hasta' ;
INC : 'inc' ;
EN : 'en' ;
MIENTRAS : 'mientras' ;
ROMPER : 'romper' ;
CONTINUAR : 'continuar' ;
LEER : 'leer' ;
IMP : 'imp' ;
IMPORTAR : 'importar' ;
COMO : 'como' ;
SET : 'set' ;
DICT : 'dict' ;
BOOL : 'verdadero' | 'falso' ;
NULL : 'nulo' ;
Y : 'y' ;
O : 'o' ;
NO : 'no' ;
IN : 'in' ;
PIPE : '|>' ;
DOTMUL : '.*' ;
INC_OP : '++' ;
DEC_OP : '--' ;

PLUS : '+' ;
MINUS : '-' ;
MUL : '*' ;
DIV : '/' ;
MOD : '%' ;
POW : '**' ;
EQ : '==' ;
NE : '!=' ;
LT : '<' ;
LE : '<=' ;
GT : '>' ;
GE : '>=' ;

NUMBER : [0-9]+ ('.' [0-9]+)? ;
STRING : '"' ( '\\' . | ~["\\] )* '"' | '\'' ( '\\' . | ~['\\] )* '\'' ;
ID : [a-zA-Z_][a-zA-Z0-9_]* ;
COMMENT : '#' ~[\r\n]* -> skip ;
NEWLINE : '\r'? '\n' ;
WS : [ \t]+ -> skip ;
