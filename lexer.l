%{
#include "parser.tab.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

extern int yylval;
void yyerror(const char *s);
%}

%option yylineno

%%
[ \t]+               ;  // Ignore whitespaces
\n                   { printf("EOL\n"); return EOL; }
"{"                  { printf("LBRACE\n"); return LBRACE; }
"}"                  { printf("RBRACE\n"); return RBRACE; }
"var"                { printf("VAR\n"); return VAR; }
"Println"            { printf("PRINTLN\n"); return PRINTLN; }
"if"                 { printf("IF\n"); return IF; }
"else"               { printf("ELSE\n"); return ELSE; }
"for"                { printf("FOR\n"); return FOR; }
"Scanln"             { printf("SCANLN\n"); return SCANLN; }
"int"                { printf("TYPE_INT\n"); return TYPE_INT; }
"string"             { printf("TYPE_STRING\n"); return TYPE_STRING; }
"bra"                { printf("TYPE_BRA\n"); return TYPE_BRA; } 
"ket"                { printf("TYPE_KET\n"); return TYPE_KET; }
"braket"             { printf("TYPE_BRAKET\n"); return TYPE_BRAKET; }
"||"                 { printf("OR\n"); return OR; }
"&&"                 { printf("AND\n"); return AND; }
"=="                 { printf("EQ\n"); return EQ; }
">"                  { printf("GT\n"); return GT; }
"<"                  { printf("LT\n"); return LT; }
"+"                  { printf("PLUS\n"); return PLUS; }
"-"                  { printf("MINUS\n"); return MINUS; }
"."                  { printf("DOT\n"); return DOT; }
"*"                  { printf("MUL\n"); return MUL; }
"/"                  { printf("DIV\n"); return DIV; }
"!"                  { printf("NOT\n"); return NOT; }
"="                  { printf("ASSIGN\n"); return ASSIGN; }
";"                  { printf("SEMICOLON\n"); return SEMICOLON; }
"("                  { printf("LPAREN\n"); return LPAREN; }
")"                  { printf("RPAREN\n"); return RPAREN; }
"|"                  { printf("PIPE\n"); return PIPE; }
[a-zA-Z_][a-zA-Z0-9_]* { printf("IDENTIFIER: %s\n", yytext); return IDENTIFIER; }
[0-9]+               { printf("NUMBER: %s\n", yytext); return NUMBER; }
\"[^"]*\"            { printf("STRING_LITERAL: %s\n", yytext); return STRING_LITERAL; }
.                    { printf("UNKNOWN (%c)\n", *yytext);}
%%

int yywrap(void) {
    return 1;
}

