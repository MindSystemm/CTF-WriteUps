Name : Baby RE\
Difficulty : 1/10\
Link : https://app.hackthebox.eu/challenges/92 \
Description : *Show us your basic skills! (P.S. There are 4 ways to solve this, are you willing to try them all?)*\

**Solution** : 

This is maybe the easiest reversing challenge you can solve. 

First, download the file on linux or whatever you want
Then, to execute it, use sudo **chmod +x baby**, now you can execute it by using **sudo ./baby**
You'll see it asks you for a key so input something 

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
