// Compile with: gcc -m64 xorneg64.c -masm=intel -o xorneg64 (Linux)

#include <stdio.h>
#include <stdint.h>

uint64_t strAddress;

// Note: text_obfs.py is normally used to obfuscate strings pushed on the stack, thus it automatically treats them as "little-endian" strings
// However, if you use text_obfs.py to obfuscate a XOR key with the NEG method (for example), the key stays in the register and never gets pushed on the stack: thus it should'nt be treated as little-endian, but our script doesn't know that!
// That's why if you want to obfuscate a XOR key with the NEG method, you should write the key characters in reverse order yourself!

// Tutorial:
// 1) Obfuscate the XOR key with NEG method (write key chars in reverse order): ./text_obfs.py -m neg -a 64 -s $'\uef\ube\uad\ude\uef\ube\uad\ude' (on Linux)
//    [*] Output: key obfuscated with NEG method. Take the second number printed, as the first one is nullbyte + random chars that aren't necessary here
//
// 2) Obfuscate the string with XOR method using the cleartext key: ./text_obfs.py -m xor -a 64 -s "J0hn_C3n4{U_Can't_Strings_Me}" -k "deadbeefdeadbeef"
//    [*] Output: numbers to be pushed on the stack

int main(int argc, char *argv[]) {
	asm("movabs rcx, 0x2152411021524111\n"
	"neg rcx\n"
	); //XOR key obfuscated with NEG method --> gets deobfuscated with the NEG instruction
	
	//there are numbers representing the obfuscated string
	//they get deobfuscated with the deobfuscated/cleartext XOR key
	asm("movabs rdx, 0x7080be92bbe0e19c\n"
	"xor rdx, rcx\n"
	"push rdx\n");

	asm("movabs rdx, 0xb9c3d79daafee19b\n"
	"xor rdx, rcx\n"
	"push rdx\n");
	
	asm("movabs rdx, 0xf9c3dfac81f8c5db\n"
	"xor rdx, rcx\n"
	"push rdx\n");
	
	asm("movabs rdx, 0xb09efdb0b0c58ea5\n"
	"xor rdx, rcx\n"
	"push rdx\n");
	
	asm("mov %[varA], rsp" //RSP points on the deobfuscated string we just pushed, so let's copy this address in our strAddress variable
	: [varA] "=r"(strAddress)
	);
	
    printf("Secret string: %s\n", strAddress);
    return 0;
 };