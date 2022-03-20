Name : RsaCtfTool\
Difficulty : 4/10\
Link : https://app.hackthebox.com/challenges/rsactftool\
Description : *Crypto is fun ;)*\

**Solution** : 

We are givan 3 files (flag.txt.aes, key & pubkey.pem). As the title is RsaCtfTool (a known tool to solve RSA-ctf challenges), we'll begin 
with decrypting the pubkey.pem (I use the frist online tool when typing decrypt pem) 

<p align="center">
  <img src="https://user-images.githubusercontent.com/26023804/110243530-12420480-7f5b-11eb-8409-f89b125cc96d.png">
</p>

The first thing you should try in that case is using **strings baby** to dump all the strings from the binary file, if you scroll, you'll see the password appearing

<p align="center">
  <img src="https://user-images.githubusercontent.com/26023804/110243574-47e6ed80-7f5b-11eb-8ec1-fced0c450753.png">
</p>

Just restart the binary and input this strings as password and you'll get the flag.

But as the owner doesn't want to use that way, we can also decompile the file using Ghidra, IDA, ... Once again, it's obvious

<p align="center">
  <img src="https://user-images.githubusercontent.com/26023804/110243733-eb380280-7f5b-11eb-880b-eb5268f5ae57.png">
</p>
