Name : Baby RE\
Difficulty : 1/10\
Link : https://app.hackthebox.eu/challenges/179 \
Description : *Who needs session integrity these days?* \
**Hint**:
Maybe you could simulate admin by modifying cookies?

**Solution** : 

<p align="center">
  <img src="https://user-images.githubusercontent.com/26023804/110695678-74fcff80-81ea-11eb-8de6-f9c46300fc6b.png">
</p>
So we're given a website with 2 options : Register & Login. 
First step would be to check the source code but nothing interesting in it...
So I tried to register as admin and I got as answer that this username was already in use so nice, we know that there's an admin user :tada:

<p align="center">
  <img src="https://user-images.githubusercontent.com/26023804/110695564-57c83100-81ea-11eb-9ea5-32a08e1553fa.png">
</p>

So let's register with a easy-to-remember username password combination (123:123). Login and you'll see that there's a cookie which was created \


<p align="center">
  <img src="https://user-images.githubusercontent.com/26023804/110695903-b68daa80-81ea-11eb-9451-af3a62d61fda.png">
</p>

Let's make some magic and try to decode it as base64 \


<p align="center">
  <img src="https://user-images.githubusercontent.com/26023804/110696003-d329e280-81ea-11eb-93ab-d065b91c8412.png">
</p>

The last step is to now convert **{"username":"admin"}** to base 64 and modify the cookie using developpers tools of whatever your want.
Then login and you'll see the flag. 

