// Compile with: gcc -m32 testneg32.c -masm=intel -o testneg32.exe (Windows)

#include <stdio.h>
#include <stdint.h>

int strAddress;

int main(int argc, char *argv[]) {
	asm("mov edx, 0xa689ff83\n"
	"neg edx\n"
	"push edx\n");

	asm("mov edx, 0x9ab2a08d\n"
	"neg edx\n"
	"push edx\n");
	
	asm("mov edx, 0x9891968e\n"
	"neg edx\n"
	"push edx\n");
	
	asm("mov edx, 0x8baca08c\n"
	"neg edx\n"
	"push edx\n");
	
	asm("mov edx, 0xd8919ebd\n"
	"neg edx\n"
	"push edx\n");
	
	asm("mov edx, 0xa0aa84cc\n"
	"neg edx\n"
	"push edx\n");
	
	asm("mov edx, 0x91ccbca1\n"
	"neg edx\n"
	"push edx\n");

	asm("mov edx, 0x9197cfb6\n"
	"neg edx\n"
	"push edx\n");
	
	asm("mov %[varA], esp" //ESP points on the deobfuscated string we just pushed, so let's copy this address in our strAddress variable
	: [varA] "=r"(strAddress)
	);
	
	//compiling on gcc Windows (mingw), the deobfuscated string pushed on the stack was overwritten by instructions preparing arguments for the call to printf()
	//to solve the problem, we reserve 8 bytes on the stack so that arguments get written here, and not on our string
	asm("sub esp, 8");
	
    printf("Secret string: %s\n", strAddress);
    return 0;
 };