from dexparser import DEXParser
import json
import requests
import base64
from Crypto.Cipher import AES
import hashlib

def Sorting(lst):
    lst.sort(key=len)
    return lst

def AES_Decrypt(data):
	unb64_ciphertext = base64.b64decode(data.encode())
	iv = unb64_ciphertext[0:16]
	unb64_ciphertext = unb64_ciphertext[16:]

	decryption_cipher = AES.new("ca1111c9f4a92797".encode('ascii'), AES.MODE_CBC, iv=iv)
	output_data = base64.b64decode(decryption_cipher.decrypt(unb64_ciphertext))
	return output_data
	
def bruteforce(a, b):
	result = 0
	for i in range(100000, 999999):
		index = str(i)
		text = a + index + b + "de287e29a4a38788ba96136d6c2f21d0"
		m = hashlib.sha512(text.encode('UTF-8'))
		if m.hexdigest() == c:
			print(i)			
			result = i
			break
	return result
url = "http://99.81.5.42:9009/getvault"
url2 = "http://99.81.5.42:9009/submitkey"
data = json.loads(requests.get(url).text)["vault"] #Getting vault from json
output_data = AES_Decrypt(data) #decrypting the vault
#Writing dex 
f = open("./decryted.dex", "wb")
f.write(output_data)
f.close()
#Parsing dex
filedir = '/home/kali/Desktop/decryted.dex'
dex = DEXParser(filedir=filedir)
string_dex = dex.get_strings()
string_dex = Sorting(string_dex)
string_dex.reverse()
#We know that d is the longest, c the second longest and for a & b we must try both possibilities 
#names are not the same here as in the dex 
b = str(string_dex[2].decode())
a = str(string_dex[3].decode())
c = str(string_dex[1].decode())
d = str(string_dex[0].decode())
#trying first possibility
result = bruteforce(a, b)
#trying other possibility if not found
if result == 0:
	result = bruteforce(b, a)
# sending our request to get the flag
x = {
  "pin": str(result),
  "vault": str(d)
}
y = json.dumps(x)
x = requests.post(url2, data  = y)
result = json.loads(x.text)["response"]
output_data = AES_Decrypt(result)
print(output_data.decode('utf-8'))
