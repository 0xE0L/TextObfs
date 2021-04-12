// Compile with: gcc -m64 testneg64.c -masm=intel -o testneg64 (Linux)

#include <stdio.h>
#include <stdint.h>

uint64_t strAddress;

int main(int argc, char *argv[]) {
	asm("movabs rax, 0xb02fff829ab2a08d\n"
	"neg rax\n"
	"push rax\n");

	asm("movabs rax, 0x9891968d8baca08c\n"
	"neg rax\n"
	"push rax\n");
	
	asm("movabs rax, 0xd8919ebca0aa84cc\n"
	"neg rax\n"
	"push rax\n");

	asm("movabs rax, 0x91ccbca09197cfb6\n"
	"neg rax\n"
	"push rax\n");
	
	asm("mov %[varA], rsp" //RSP points on the deobfuscated string we just pushed, so let's copy this address in our strAddress variable
	: [varA] "=r"(strAddress)
	);
	
    printf("Secret string: %s\n", strAddress);
    return 0;
 };