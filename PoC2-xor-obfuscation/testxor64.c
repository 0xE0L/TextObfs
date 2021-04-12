// Compile with: gcc -m64 testxor64.c -masm=intel -o testxor64 (Linux)

#include <stdio.h>
#include <stdint.h>

uint64_t strAddress;

int main(int argc, char *argv[]) {
	asm("movabs rcx, 0xdeadbeefefbeadde"); //key used to UNXOR the string
	
	asm("movabs rdx, 0x21c6be928af3f2ad\n"
	"xor rdx, rcx\n"
	"push rdx\n");

	asm("movabs rdx, 0xb9c3d79d9bedf2aa\n"
	"xor rdx, rcx\n"
	"push rdx\n");
	
	asm("movabs rdx, 0xf9c3dfacb0ebd6ea\n"
	"xor rdx, rcx\n"
	"push rdx\n");
	
	asm("movabs rdx, 0xb09efdb081d69d94\n"
	"xor rdx, rcx\n"
	"push rdx\n");
	
	asm("mov %[varA], rsp" //RSP points on the deobfuscated string we just pushed, so let's copy this address in our strAddress variable
	: [varA] "=r"(strAddress)
	);
	
    printf("Secret string: %s\n", strAddress);
    return 0;
 };