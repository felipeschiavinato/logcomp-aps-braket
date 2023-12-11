python main.py teste.go
nasm -f elf -o program.o teste.asm
gcc -m32 -no-pie -o program program.o
./program