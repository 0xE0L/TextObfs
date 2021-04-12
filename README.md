# TextObfs

TextObfs is a little project to assist you in obfuscating strings that will be directly hardcoded in instructions (in .text section), thus throwing away the need to use variables or .data/.bss section of a binary.

## Purpose

Storing strings directly in instructions (in .text section) can be interesting in some cases, particularly when using shellcodes.
Strings can be obfuscated using different methods, currently it supports NEG method ([see](https://www.aldeid.com/wiki/X86-assembly/Instructions/neg)) or classic XOR method using a XOR key.

It can obfuscate a string by returning it as (obfuscated) numbers, but also undo what it has done by taking numbers in argument and printing the deobfuscated string.
Please note it remains up to the user to include obfuscated numbers (representing the string) in its program/shellcode and do the on-the-fly deobufscation job. It's not TextObfs job to automatically generate a corresponding source code, binary or shellcode including your strings. However, examples/PoCs are provided with the repository to help you understand what you can do with that.

Please note the obfuscation level here remains low as we will see in the detection section.
It will bypass simple scanning of strings (like `strings` command), but any beginner reverser or simple string deobfuscator will easily retrieve the obfuscated strings.

## Example

To obfuscate a string using XOR method, use the command: `./text_obfs.py -m xor -a 64 -s "My_S3cr3t_String" -k deadbeefdeadbeef`.\
Output:
```
[*] 0x997295bdc88961ef    |ß$R+ßG|
[*] 0xb9c3d79daafee19b    |t_String|
[*] 0xeddfdddc8df2c7a2    |My_S3cr3|
```
A nullbyte is automatically added at the end of the string, then random junk chars are added after the nullbyte (won't be displayed in C style programs) to pad the last number to a register's size.

You can undo this (helpful if you need to reverse a binary or shellcode) by doing: `./text_obfs.py -m xor -a 64 -d 0x997295bdc88961ef 0xb9c3d79daafee19b 0xeddfdddc8df2c7a2 -k deadbeefdeadbeef`.\
Output:
```
[+] (Xor) String deobfuscated (64 bits): 'My_S3cr3t_String'
```

Same principle applies to NEG method although you don't even need to use the `--key` option.\
As you will see in PoCs you can combine 2 methods, for example by obfuscating a XOR key with the NEG method, then unXOR obfuscated numbers using the deobfuscated key.

## Detection

As of April 2021 I checked my 3 PoCs variants after [FLOSS](https://github.com/fireeye/flare-floss) and IDA-Pro, and both of them were able to statically retrieve the string for every variant. As discussed below, it means this is far from being a strong obfuscation method.

If you wanted a stronger obfuscation method in binaries (not shellcode), I'll suggest using classical methods using some "cipher" algorithms (XOR, RC4) and a key stored in a uninitialized variable (.bss section). The key would be written in the variable at execution time using an heavily obufscated function (with [OLLVM](https://github.com/obfuscator-llvm/obfuscator) for example).
Thus it would be much harder to statically retrieve the key and the string, even using tools automating this task.
