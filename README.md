# logcomp-aps-braket

## EBNF
```
PROGRAM = { STATEMENT };
BLOCK = "{", "\n", { STATEMENT }, "}";
STATEMENT = ( λ | ASSIGNMENT | PRINT | IF | FOR | VARDEC | KET | BRA | BRAKET), "\n" ;
VARDEC = "var", IDENTIFIER, TYPE, (λ | ("=", BOOLEAN_EXPRESSION));
ASSIGNMENT = IDENTIFIER, "=", BOOLEAN_EXPRESSION ;
PRINT = "Println", "(", BOOLEAN_EXPRESSION, ")" ;
IF = "if", BOOLEAN_EXPRESSION, BLOCK, (λ | ("else", BLOCK));
FOR = "for", ASSIGNMENT, ";", BOOLEAN_EXPRESSION, ";", ASSIGNMENT, BLOCK;
BOOLEAN_EXPRESSION = BOOLEAN_TERM, {"||", BOOLEAN_TERM}; 
BOOLEAN_TERM = RELATIVE_EXPRESSION, {"&&", RELATIVE_EXPRESSION}; 
RELATIVE_EXPRESSION = EXPRESSION, {("==" | ">" | "<"), EXPRESSION}; 
EXPRESSION = TERM, { ("+" | "-" | "."), TERM } ;
TERM = FACTOR, { ("*" | "/"), FACTOR } ;
FACTOR = (("+" | "-" | "!"), FACTOR) | NUMBER | STRING | ("(", BOOLEAN_EXPRESSION, ")") | IDENTIFIER | ("Scanln", "(", ")") | KET | BRA ;
IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;
TYPE = "int" | "string";
STRING = """, { LETTER }, """;
NUMBER = DIGIT, { DIGIT } ;
LETTER = ( a | ... | z | A | ... | Z ) ;
DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;
BINARY_DIGIT = ( 0 | 1 ) ;
BINARY_SEQUENCE = BINARY_DIGIT, { BINARY_DIGIT } ;
KET = "|", BINARY_SEQUENCE, "⟩" ;
BRA = "⟨", BINARY_SEQUENCE, "|" ;
BRAKET = "⟨", BINARY_SEQUENCE, "|", BINARY_SEQUENCE, "⟩" ;

```
