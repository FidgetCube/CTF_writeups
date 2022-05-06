# crackMe2 (Reversing 50 points) 

## Description

Time for some basic algebra...

<p align="center"><img src="_images/description.png"></p>

## Resources

[Download file](https://ctf.b01lers.com/download?file_key=fd2e5d90781cff1dad8585eea24ea5cfa2249a85588ddb9396a3d3f92bfaf20e&team_key=f525c3a1714f99e5c9c69495b11064d465f4c80aa98c6bae8d663f031246aff7)

## Solution

This challenge and solution is very similar to the last crackMe challenge. [You can read the writeup here for the Ghidra guide.](https://github.com/FidgetCube/CTF_writeups/tree/main/2022-bo1lersCTF/crackme(reversing)#readme)

Similar to the last challenge, in the wild you should never execute a binary if you do not know what it does. CTFs are a slightly lower risk but there is still a chance it could harm your computer so *RUN IT AT YOUR OWN RISK*.

For this CTF challenge, i ran the binary and it propmts the user for a product key and performs some form of validation on  whatever you enter, testing for the correct product key. So lets open it up and attempt to reverse the validation of user input to pull out the correct key.

Open up Ghidra, create a new project and load the downloaded binary. Open the binary in the code browser tool. Looking at the Symbol Tree on the left hand side you can see a list of functions, and one that immediately jumps out is check().  

<p align="center"><img src="_images/ghidra.png"></p>

Clicking on the check() function reveals the code in the Decompiler on the right hand side. Here you can see the function has one argument passed to it *param_1* which will be the stored user input from the prompt when the binary is run. 

Lets explain what this does in a nutshell. The function iterates over each individual character of the input performing a test, if the test passes it steps into a nested *if* statement that tests the next character in order. If the test fails due to being the wrong character, the code jumps out, stops testing and prints an error. Looking at the tests, we can see there is 14 checks performed so we know the correct key is 14 characters in length, remembering that arrays are indexed from 0 so the checks are performed as 0-13 (param_1[0] = 1st character and param_1[5] = 6th character etc). Characters 12, 13 and 14 are referenced using hexidecimal notation (0xb = 11 in decimal) to try and obscure the equation a little more but it's pretty basic and easy to convert to decimal, param_1[0xb] = param_1[11] = 12th character. 

<p align="center"><img src="_images/check().png"></p>

We can see that most of the characters in the tests are hard coded here so we can see exactly what the first 10 characters are, as well as the last 2. The \* denotes an unknown character for the 10th and 11th characters where the correct character isn't immediately clear because there is some algebraic equation that we will need to solve to get the answer rather than bute forcing these 2 characters. 
 
0 = b   
1 = c  
2 = t  
3 = f  
4 = {  
5 = 4  
6 = l  
7 = g  
8 = 3  
9 = b  
10 = *  
11 = *  
12 = !  
13 = }  
The flag so far is bctf{4lg3b**!}

Character 11:
```
if ((byte)(param_1[10] ^ param_1[9]) == 0x10)
```
^ is the symbol for the XOR operation  
param_1[9] = 'b'  
0x10 = 16 in decimal  

So this translates to 
```
if (x XOR 'b' == 16)
```                
We know that XOR operations are reversible so (x XOR 'b' == 16) is the same as ('b' XOR 16 == x).  
Time for some quick python to solve this.  
The ord() function takes a character and returns its decimal ASCII value.  ord('b') = 98  
98 ^ 16 = 114  
The chr() takes a decimal value and converts it to its ASCII character. chr(114) = 'r'  

So our flag progress is now bctf{4lg3br*!}

<p align="center"><img src="_images/algebraXOR.png"></p>

Character 12:
```
if (param_1[0xb] + -1 == (int)param_1[8])
```
This translates to
```
if (param_1[11] + -1 == 3
if (x -1 == 3)
x = 4
```
 
So our 12th character is '4' which completes the flag

## flag = bctf{4lg3br4!}
