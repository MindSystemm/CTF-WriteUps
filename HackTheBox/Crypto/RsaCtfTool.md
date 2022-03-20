-- Under construction -- 

Name : RsaCtfTool\
Difficulty : 4/10\
Link : https://app.hackthebox.com/challenges/rsactftool \
Description : Crypto is fun ;)

**Solution** : 

We are given 3 files (flag.txt.aes, key & pubkey.pem). As the title is RsaCtfTool (a known tool to solve RSA-ctf challenges), we'll begin 
with decrypting the pubkey.pem. For that, we can use the following openssl command : openssl rsa -pubin -in pubkey.pem -text\
There we're given the modulus (n) = 1128137999850045612492145429133282716267233566834715456536184965477269592934207986950131365518741418540788596074115883774105736493742449131477464976858161587355643311888741515506653603321337485523828144179637379528510277430032789458804637543905426347328041281785616616421292879871785633181756858096548411753919440011378411476275900648915887370219369154688926914542233244450724820670256654513052812215949495598592852131398736567134556141744727764716053145639513031 and the public exponent (e) = 65537. The next step is trying to factorize n so I looked on Factordb and we can see that n is 10410080216253956216713537817182443360779235033823514652866757961082890116671874771565125457104853470727423173827404139905383330210096904014560996952285911 ^3 so we can now assume that p = 10410080216253956216713537817182443360779235033823514652866757961082890116671874771565125457104853470727423173827404139905383330210096904014560996952285911 ^2 and q = 10410080216253956216713537817182443360779235033823514652866757961082890116671874771565125457104853470727423173827404139905383330210096904014560996952285911 as p * q should be equal to n 
The next RSA constant we can find is phi which is (p-1) * (q-1) and thanks to phi, we can find d, which is inverse of e modulus phi (the command inverse(e, phi) in python gives us d. We know have all datas to decrypt the key file by taking key to the power d modulus n and we have now the AES key to decrypt our flag. I only did it with the following python command : cipher = AES.new(M, AES.MODE_ECB) then m = cipher.decrypt(c) with M = decoded rsa text and c the content of the flag.txt.aes 
