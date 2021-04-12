#!/bin/python3

import argparse
import random


### Support functions

def bitwise_not(numBin):
    numBinNegated = ""
    for i in numBin:
        if i=='1':
            numBinNegated += "0"
        else:
            numBinNegated += "1"
    return numBinNegated

def wrap_custom(string, n):
    return [string[i:i+n] for i in range(0, len(string), n)]


### Frontend functions

# Takes a string to be obfuscated in 1st argument
# Returns a list of 32/64 bits hexadecimal numbers, which represent the obfuscated string
# Numbers are presented in the order where they need to be pushed on the stack

def obfuscate_neg(string, bitsNb):
    # check if architecture is 32 or 64 bits
    if not (bitsNb==32 or bitsNb==64):
        print("[!] Error: only 32 and 64 bits numbers are supported")
        return 1

    # if nullbyte not present at the end of the string, we add it
    if string[-1:] != '\x00':
        string += '\x00'

    # we separate the string in substrings, where each substring's maximum length corresponds to the 'bitsNb' architecture (in bytes)
    substringsList = wrap_custom(string, int(bitsNb/8))
    
    # if the last substring's length isn't equal to 32/64 bytes, we pad it with random chars (it doesn't matter which ones, as a nullbyte is placed before they won't be displayed by C)
    # we could also pad it with nullbytes, but I think adding random chars instead adds more obfuscation
    while len(substringsList[-1]) != int(bitsNb/8):
        substringsList[-1] += chr(random.randint(0,255))

    print("[+] (Neg) Obfuscated string represented in hexadecimal", bitsNb, "bits numbers!\nThey have to be pushed in this order on the stack (deobfuscate with NEG before pushing):")
    substringsObfsList = []
    # we parse the list in reverse order as substrings needs to be pushed like this on the stack
    # first substring displayed = first substring that needs to be pushed on the stack i.e.
    for substring in reversed(substringsList):
        hexSubstring=""
        # we convert the substring to its hexadecimal representation
        # we parse every char in reverse order as x86 is little-indian
        for char in reversed(substring):
            hexSubstring += '{:0>2x}'.format(ord(char))

        numDec = int(hexSubstring, 16) # we then convert the hexadecimal number to decimal

        # let's do the opposite of a NEG instruction
        numDec -= 1 # substract one to it
        numBin = bin(numDec)[2:].zfill(bitsNb) # we convert the number to a 'bitsNb'-bits binary number
        numBinObfs = bitwise_not(numBin) # bitwise not on the number
        numHexObfs = hex(int(numBinObfs, 2)) # convert it back to hex
        
        substringsObfsList.append(numHexObfs) # add the obfuscated substring to the list that will be returned
        print("   [*]", numHexObfs, "   |"+substring+"|")

    return substringsObfsList

# Takes a list of 32/64 bits hexadecimal numbers: elements have to be provided in the same order as numbers are pushed on the stack
# Returns the deobfuscated string, where every char after nullbyte has been removed (C-like)

def deobfuscate_neg(userInputsList, bitsNb):
    # check if architecture is 32 or 64 bits
    if not (bitsNb==32 or bitsNb==64):
        print("[!] Error: only 32 and 64 bits numbers are supported")
        return 1
    
    completeString = ""
    # we parse the list in reverse order as substrings were pushed like this on the stack
    for number in reversed(userInputsList):        
        # check if a hexadecimal number size indeed corresponds to the selected architecture (32 or 64 bits)
        # if hexadecimal string has '0x' prefix (with or without it is supported), we exclude it from the len() process
        if (number.startswith('0x')):
            if len(number[2:]) > (bitsNb/4) or len(number[2:]) < 1:
                print("[!] Error: number", number, "doesn't correspond to a", bitsNb, "bits string")
                return 1
        else:
            if len(number) > (bitsNb/4) or len(number) < 1:
                print("[!] Error: number", number, "doesn't correspond to a", bitsNb, "bits string")
                return 1
        
        # determine if the number is a valid hexadecimal string
        try:
            numDec = int(number, 16)
        except:
            print("[!] Error:", number, "is not a valid hexadecimal string")
            return 1
        
        # real function begins here
        numBin = bin(numDec)[2:].zfill(bitsNb) # we convert the number to a 'bitsNb'-bits binary number
        
        # we do the equivalent of a NEG instruction
        numBinNegated = bitwise_not(numBin) # bitwise not on the number
        numIntNegated = int(numBinNegated, 2) # convert it back to int
        numIntNegated += 1 # add one to it
        numHexList = wrap_custom(hex(numIntNegated)[2:], 2) # we convert it back to hex and we split every byte in a different element on the list (numHexList = ['ef', 'be', 'ad', 'de'] i.e.)

        # we parse every byte in reverse order as x86 is little-indian
        subString = ""
        for char in reversed(numHexList):
            subString += chr(int(char, 16))
        completeString += subString

    # as in C, we don't want to print what's after the nullbyte ('\x00')
    index = completeString.find('\x00')
    if index != -1:
        completeString = completeString[:index] # so we remove what's after the first nullbyte
    
    print("[+] (Neg) String deobfuscated ("+str(bitsNb)+" bits):", "'"+completeString+"'")
    return completeString

# Takes a string to be obfuscated in 1st argument, and a XOR key in 2nd argument (to encrypt the string with)
# Returns a list of 32/64 bits hexadecimal numbers, which represent the obfuscated string (encrypted with the key)
# Numbers are presented in the order where they need to be pushed on the stack
# For the sake of simplicity, 1) key must be provided in hexadecimal representation and 2) key length must match with the size of a register (can't be less/more than 32/64 bits)
# If you want to change this behaviour (provide a key with size of the whole string and not just the size of a substring), this could easily be adapted

def obfuscate_xor(string, key, bitsNb):
    # check if architecture is 32 or 64 bits
    if not (bitsNb==32 or bitsNb==64):
        print("[!] Error: only 32 and 64 bits numbers are supported")
        return 1

    # determine if the key is a valid hexadecimal string
    try:
        int(key, 16)
    except:
        print("[!] Error:", key, "is not a valid hexadecimal string")
        print("Keys must be provided in hexadecimal format (i.e. 'deadbeef' in 32 bits or '00112233deadbeef' in 64 bits)!")
        return 1

    # check if key length == 32 or 64 bits
    # if hexadecimal string has '0x' prefix (with or without it is supported), we exclude it from the len() process
    if (key.startswith('0x')):
        if len(key[2:]) != (bitsNb/4):
            print("[!] Error: key", key, "doesn't correspond to a", bitsNb, "bits number")
            print("Key length MUST be", int(bitsNb/8), "bytes (can't be less or more)!")
            return 1
    else:
        if len(key) != (bitsNb/4):
            print("[!] Error: key", key, "doesn't correspond to a", bitsNb, "bits number")
            print("Key length MUST be", int(bitsNb/8), "bytes (can't be less or more)!")
            return 1

    # if nullbyte not present at the end of the string, we add it
    if string[-1:] != '\x00':
        string += '\x00'

    # we separate the string in substrings, where each substring's maximum length corresponds to the 'bitsNb' architecture (in bytes)
    substringsList = wrap_custom(string, int(bitsNb/8))
    
    # if the last substring's length isn't equal to 32/64 bytes, we pad it with random chars (it doesn't matter which ones, as a nullbyte is placed before they won't be displayed by C)
    # we could also pad it with nullbytes, but I think adding random chars instead adds more obfuscation
    while len(substringsList[-1]) != int(bitsNb/8):
        substringsList[-1] += chr(random.randint(0,255))
    
    print("[+] (Xor) Obfuscated string represented in hexadecimal", bitsNb, "bits numbers!\nThey have to be pushed in this order on the stack (deobfuscate with 'XOR RegisterNumber, RegisterKey' before pushing):")
    substringsObfsList = []
    # we parse the list in reverse order as substrings needs to be pushed like this on the stack
    # first substring displayed = first substring that needs to be pushed on the stack i.e.
    for substring in reversed(substringsList):
        hexSubstring=""
        # we convert the substring to its hexadecimal representation
        # we parse every char in reverse order as x86 is little-indian
        for char in reversed(substring):
            hexSubstring += '{:0>2x}'.format(ord(char))

        # we XOR the substring with the key
        numHexObfs = hex(int(hexSubstring, 16) ^ int(key, 16))

        # weadd the obfuscated substring to the list that will be returned
        substringsObfsList.append(numHexObfs)
        print("   [*]", numHexObfs, "   |"+substring+"|")

    return substringsObfsList

# Takes a list of 32/64 bits hexadecimal numbers as 1st argument: elements have to be provided in the same order as numbers are pushed on the stack
# Takes the XOR key to unxor/decrypt the numbers with on 2nd argument
# Returns the deobfuscated string, where every char after nullbyte has been removed (C-like)

def deobfuscate_xor(userInputsList, key, bitsNb):
    # check if architecture is 32 or 64 bits
    if not (bitsNb==32 or bitsNb==64):
        print("[!] Error: only 32 and 64 bits numbers are supported")
        return 1

    # determine if the key is a valid hexadecimal string
    try:
        keyDec = int(key, 16)
    except:
        print("[!] Error:", key, "is not a valid hexadecimal string")
        print("Keys must be provided in hexadecimal format (i.e. 'deadbeef' in 32 bits or '00112233deadbeef' in 64 bits)!")
        return 1

    # check if key length == 32 or 64 bits
    # if hexadecimal string has '0x' prefix (with or without it is supported), we exclude it from the len() process
    if (key.startswith('0x')):
        if len(key[2:]) != (bitsNb/4):
            print("[!] Error: key", key, "doesn't correspond to a", bitsNb, "bits number")
            print("Key length MUST be", int(bitsNb/8), "bytes (can't be less or more)!")
            return 1
    else:
        if len(key) != (bitsNb/4):
            print("[!] Error: key", key, "doesn't correspond to a", bitsNb, "bits number")
            print("Key length MUST be", int(bitsNb/8), "bytes (can't be less or more)!")
            return 1
    
    completeString = ""
    # we parse the list in reverse order as substrings were pushed like this on the stack
    for number in reversed(userInputsList):        
        # check if a hexadecimal number size indeed corresponds to the selected architecture (32 or 64 bits)
        # if hexadecimal string has '0x' prefix (with or without it is supported), we exclude it from the len() process
        if (number.startswith('0x')):
            if len(number[2:]) > (bitsNb/4) or len(number[2:]) < 1:
                print("[!] Error: number", number, "doesn't correspond to a", bitsNb, "bits string")
                return 1
        else:
            if len(number) > (bitsNb/4) or len(number) < 1:
                print("[!] Error: number", number, "doesn't correspond to a", bitsNb, "bits string")
                return 1
        
        # determine if the number is a valid hexadecimal string
        try:
            numDec = int(number, 16)
        except:
            print("[!] Error:", number, "is not a valid hexadecimal string")
            return 1
        
        # real function begins here
        numDecUnxored = numDec ^ keyDec # we UNXOR the number with the key
        numHexList = wrap_custom(hex(numDecUnxored)[2:], 2) # we convert it back to hex and we split every byte in a different element on the list (numHexList = ['ef', 'be', 'ad', 'de'] i.e.)

        # we parse every byte in reverse order as x86 is little-indian
        subString = ""
        for char in reversed(numHexList):
            subString += chr(int(char, 16))
        completeString += subString

    # as in C, we don't want to print what's after the nullbyte ('\x00')
    index = completeString.find('\x00')
    if index != -1:
        completeString = completeString[:index] # so we remove what's after the first nullbyte
    
    print("[+] (Xor) String deobfuscated ("+str(bitsNb)+" bits):", "'"+completeString+"'")
    return completeString


### Main ###

descriptionStr = """Obfuscate/deobfuscate a string using XOR or NEG methods
Obfuscating a string will return numbers that will be up to you to include in your program (see PoCs)
Numbers are crafted to be stored in registers using mov/movabs instructions, then deobfuscated on-the-fly in your program, then pushed on the stack and used"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=True, description=descriptionStr, formatter_class=argparse.RawDescriptionHelpFormatter) #this formatter_class is only used to make argparse make newlines with the description

    # those 2 args are mandatory
    parser.add_argument("-m", "--mode", type=str, choices=['neg', 'xor'], help="Choose between NEG or XOR obfuscation method", required=True)
    parser.add_argument("-a", "--arch", type=int, choices=[32, 64], help="Choose your architecture (32 or 64 bits) to define obfuscated numbers length", required=True)

    # this one is mandatory only if XOR mode is used (that's why we don't use "required" here), we will manually check that later
    parser.add_argument("-k", "--key", type=str, help="Key used to deobfuscate/obfuscate a string when using XOR mode")
    
    # required mutually_exclusive_group --> means either one of those 2 arguments must be selected, not both of them, not none of them
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-s", "--string", type=str, help="Obfuscate the string passed in argument and get obfuscated numbers")
    group.add_argument("-d", "--deobf", type=str, nargs='+', help="Deobfuscate numbers passed in argument (must be hexadecimal) and get deobfuscated string") # nargs='+' means multiple elements can be passed in argument (will be stored in a list), and a least one element must be passed

    options = parser.parse_args() # we parse all arguments
    
    # this point will never be reached if help is displayed or some conditions weren't met ("required" not used, bad type, etc)
    # if XOR mode is used but no key has been provided, we raise an error and exit the program (manual check)
    if options.mode=="xor" and options.key is None:
        parser.error('XOR key must be provided with -k/--key option when XOR mode is used')
    
    # we call different functions depending of which options were chosen
    # obfuscate
    if options.string:
        if options.mode=="neg":
            obfuscate_neg(options.string, options.arch)
        elif options.mode=="xor":
            obfuscate_xor(options.string, options.key, options.arch)

    # deobfuscate
    elif options.deobf:
        if options.mode=="neg":
            deobfuscate_neg(options.deobf, options.arch) # options.deobf is the list of numbers passed in argument
        elif options.mode=="xor":
            deobfuscate_xor(options.deobf, options.key, options.arch)
