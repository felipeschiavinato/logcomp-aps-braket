section .data
SYS_EXIT equ 1
SYS_READ equ 3
SYS_WRITE equ 4
STDIN equ 0
STDOUT equ 1
True equ 1
False equ 0
new_line: db 10

formatin:   db "%d", 0
formatout:  db "%d", 10, 0
scanint:    times 4 db 0
str_buffer: times 12 db 0  ; 10 digits + potential '-' sign + null-terminator
ten:        dd 10

section .text
global main
extern scanf, printf

itoa:
    PUSH EBX
    PUSH ECX
    PUSH EDX

    ; Check if number is negative
    TEST EAX, EAX
    JNS .positive

    ; If negative, make it positive and remember it was negative
    NEG EAX
    PUSH EAX

    ; Write '-' to buffer and move to next position
    MOV BYTE [str_buffer], '-'
    ADD DWORD [str_buffer], 1

    ; Get the original positive value back
    POP EAX

.positive:
    MOV ECX, str_buffer

.reverseLoop:
    XOR EDX, EDX
    DIV DWORD [ten]
    ADD DL, '0'
    MOV [ECX], DL
    ADD ECX, 1
    TEST EAX, EAX
    JNZ .reverseLoop

    ; Null terminate the string
    MOV [ECX], BYTE 0

    POP EDX
    POP ECX
    POP EBX
    RET

print:
    ; Convert integer in EAX to string
    CALL itoa

    ; Write the string to STDOUT
    MOV EAX, SYS_WRITE
    MOV EBX, STDOUT
    MOV ECX, str_buffer
    MOV EDX, 12
    INT 0x80
    MOV EAX, SYS_WRITE
        MOV EBX, STDOUT
        MOV ECX, new_line ; Address of the newline character
        MOV EDX, 1  ; Size of the newline character
        INT 0x80

    RET

println:  ; subrotina print

  PUSH EBP ; guarda o base pointer
  MOV EBP, ESP ; estabelece um novo base pointer

  MOV EAX, [EBP+8] ; 1 argumento antes do RET e EBP
  XOR ESI, ESI

print_dec: ; empilha todos os digitos
  MOV EDX, 0
  MOV EBX, 0x000A
  DIV EBX
  ADD EDX, '0'
  PUSH EDX
  INC ESI ; contador de digitos
  CMP EAX, 0
  JZ print_next ; quando acabar pula
  JMP print_dec

print_next:
  CMP ESI, 0
  JZ print_exit ; quando acabar de imprimir
  DEC ESI

  MOV EAX, SYS_WRITE
  MOV EBX, STDOUT

  POP ECX
  MOV [res], ECX
  MOV ECX, res

  MOV EDX, 1
  INT 0x80
  JMP print_next

print_exit:
  POP EBP
  RET

segment .bss 
res RESB 1
section .text
global main 
extern scanf 
extern printf 
binop_je :
JE binop_true
JMP binop_false
binop_jg :
JG binop_true
JMP binop_false
binop_jl :
JL binop_true
JMP binop_false
binop_false :
MOV EAX, False
JMP binop_exit
binop_true :
MOV EAX, True
binop_exit :
RET

main:
PUSH EBP
MOV EBP, ESP



POP EBP
MOV EAX, 1
INT 0x80