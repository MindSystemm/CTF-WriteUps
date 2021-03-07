Name : Bypass\
Difficulty : 2/10\
Link : https://app.hackthebox.eu/challenges/114 \
Description : *The Client is in full control. Bypass the authentication and read the key to get the Flag.*\

**Solution** : 

This file is a .net file so you can view the source code with any .net decompiler (I recommend you use dnSpy) \
After a quick look at the code, I decided to debug the exe and modify it to make him give me the flag. \
I set a BP on this method because I noticed it use writeline and then I debugged the exe and input a random user/pass combination \



<p align="center">
  <img src="https://i.ibb.co/PwhwcDg/Screenshot-2.png">
</p>

We already bypassed the first thing. I decided to put a BP on the method called in the if because I noticed it uses readline and writeline 


<p align="center">
  <img src="https://user-images.githubusercontent.com/26023804/110244670-145a9200-7f60-11eb-9148-40e1a8d54f3a.png">
</p>

Then just walk instruction by instruction and you'll see the password appearing 


<p align="center">
  <img src="https://user-images.githubusercontent.com/26023804/110244690-3227f700-7f60-11eb-893b-d120b78c3494.png">
</p>

Now just continue and input this as secret key and it'll give you the flag
