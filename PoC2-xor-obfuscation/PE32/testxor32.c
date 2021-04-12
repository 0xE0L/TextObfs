// Compile with: gcc -m32 testxor32.c -masm=intel -o testxor32.exe (Windows)

#include <stdio.h>
#include <stdint.h>

int strAddress;

int main(int argc, char *argv[]) {
	asm("mov ecx, 0xdeadbeef"); //key used to UNXOR the string
	
	asm("mov edx, 0xd099be92\n"
	"xor edx, ecx\n"
	"push edx\n");
	
	asm("mov edx, 0xbbe0e19c\n"
	"xor edx, ecx\n"
	"push edx\n");
	
	asm("mov edx, 0xb9c3d79d\n"
	"xor edx, ecx\n"
	"push edx\n");

	asm("mov edx, 0xaafee19b\n"
	"xor edx, ecx\n"
	"push edx\n");
	
	asm("mov edx, 0xf9c3dfac\n"
	"xor edx, ecx\n"
	"push edx\n");
	
	asm("mov edx, 0x81f8c5db\n"
	"xor edx, ecx\n"
	"push edx\n");
	
	asm("mov edx, 0xb09efdb0\n"
	"xor edx, ecx\n"
	"push edx\n");
	
	asm("mov edx, 0xb0c58ea5\n"
	"xor edx, ecx\n"
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