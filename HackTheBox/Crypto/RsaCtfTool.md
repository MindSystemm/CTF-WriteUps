-- Under construction -- 

Name : RsaCtfTool
Difficulty : 4/10
Link : https://app.hackthebox.com/challenges/rsactftool 
Description : Crypto is fun ;)

**Solution** : 

We are given 3 files (flag.txt.aes, key & pubkey.pem). As the title is RsaCtfTool (a known tool to solve RSA-ctf challenges), we'll begin with decrypting the pubkey.pem. For that, we can use the following openssl command : 
`openssl rsa -pubin -in pubkey.pem -text`
There we're given the modulus (n) & the public exponent (e) 

![](https://i.ibb.co/v3VSRgZ/Screenshot-3.jpg)

The next step is trying to factorize n so I looked on Factordb and we found a match !  

![](https://i.ibb.co/PYdVrd8/Screenshot-2.jpg)

We now have our p & our q.
The next RSA constant we can find is phi which is (p-1) * (q-1) and thanks to phi, we can find d, which is inverse of e modulus phi (the command inverse(e, phi) in python gives us d). We know have all datas to decrypt the key file by taking key to the power d modulus n. We have now the AES key to decrypt our flag. 
