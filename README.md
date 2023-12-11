# PortGO

## EBNF
```
PROGRAM = { STATEMENT };
BLOCK = "{", "\n", { STATEMENT }, "}";
STATEMENT = ( λ | ASSIGNMENT | PRINT | IF | FOR | VARDEC), "\n" ;
VARDEC = "var", IDENTIFIER, TYPE, (λ | ("=", BOOLEAN_EXPRESSION));
ASSIGNMENT = IDENTIFIER, "=", BOOLEAN_EXPRESSION ;
PRINT = "Imprime", "(", BOOLEAN_EXPRESSION, ")" ;
IF = "se", BOOLEAN_EXPRESSION, BLOCK, (λ | ("else", BLOCK));
FOR = "para", ASSIGNMENT, ";", BOOLEAN_EXPRESSION, ";", ASSIGNMENT, BLOCK;
BOOLEAN_EXPRESSION = BOOLEAN_TERM, {"||", BOOLEAN_TERM}; 
BOOLEAN_TERM = RELATIVE_EXPRESSION, {"&&", RELATIVE_EXPRESSION}; 
RELATIVE_EXPRESSION = EXPRESSION, {("==" | ">" | "<"), EXPRESSION}; 
EXPRESSION = TERM, { ("+" | "-" | "."), TERM } ;
TERM = FACTOR, { ("*" | "/"), FACTOR } ;
FACTOR = (("+" | "-" | "!"), FACTOR) | NUMBER | STRING | ("(", BOOLEAN_EXPRESSION, ")") | IDENTIFIER | ("Entra", "(", ")");
IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;
TYPE = "int";
NUMBER = DIGIT, { DIGIT } ;
LETTER = ( a | ... | z | A | ... | Z ) ;
DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;

```


### Exemplo 
```
variavel x inteiro
variavel y inteiro
x = 3+1
y = x
se x > 1 {
    x = 5-1
}
se (x == 3) {
} senao {
    x = 3
}
para x = 3; x < 5; x = x + 1 {
    y = x - 1
}

Imprime(x)
```

Para compilar o seu programa, garanta que esta em um ambiente Linux com python, nasm e gcc instalados. Rode o arquivo roda.sh
As etapas lexicas e sintaticas também estão implementadas com Flex e Bison, respectivamente.
