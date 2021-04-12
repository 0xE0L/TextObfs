// Compile with: gcc -m32 xorneg32.c -masm=intel -o xorneg32.exe (Windows)

#include <stdio.h>
#include <stdint.h>

int strAddress;

// Note: text_obfs.py is normally used to obfuscate strings pushed on the stack, thus it automatically treats them as "little-endian" strings
// However, if you use text_obfs.py to obfuscate a XOR key with the NEG method (for example), the key stays in the register and never gets pushed on the stack: thus it should'nt be treated as little-endian, but our script doesn't know that!
// That's why if you want to obfuscate a XOR key with the NEG method, you should write the key characters in reverse order yourself!

// Tutorial:
// 1) Obfuscate the XOR key with NEG method (write key chars in reverse order): ./text_obfs.py -m neg -a 32 -s $'\uef\ube\uad\ude' (on Linux)
//    [*] Output: key obfuscated with NEG method. Take the second number printed, as the first one is nullbyte + random chars that aren't necessary here
//
// 2) Obfuscate the string with XOR method using the cleartext key: ./text_obfs.py -m xor -a 32 -s "J0hn_C3n4{U_Can't_Strings_Me}" -k "deadbeef"
//    [*] Output: numbers to be pushed on the stack

int main(int argc, char *argv[]) {
	asm("mov ecx, 0x21524111\n"
	"neg ecx\n"
	); //XOR key obfuscated with NEG method --> gets deobfuscated with the NEG instruction
	
	//there are numbers representing the obfuscated string
	//they get deobfuscated with the deobfuscated/cleartext XOR key
	asm("mov edx, 0x4171be92\n"
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
	
	asm("mov %[varA], esp" //RSP points on the deobfuscated string we just pushed, so let's copy this address in our strAddress variable
	: [varA] "=r"(strAddress)
	);
	
	//compiling on gcc Windows (mingw), the deobfuscated string pushed on the stack was overwritten by instructions preparing arguments for the call to printf()
	//to solve the problem, we reserve 8 bytes on the stack so that arguments get written here, and not on our string
	asm("sub esp, 8");
	
    printf("Secret string: %s\n", strAddress);
    return 0;
 };