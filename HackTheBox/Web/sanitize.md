Name : Sanitize\
Difficulty : 0/10\
Link : https://app.hackthebox.eu/challenges/178 \
Description : *Can you escape the query context and log in as admin at my super secure login page?* \

**Hint**:
Easiest sql injection i've ever seen 

**Solution** : 

<p align="center">
  <img src="https://user-images.githubusercontent.com/26023804/110697264-67e11000-81ec-11eb-94c9-0780a1ed9f24.png">
</p>

We're given a login page so let's login with the classic admin:admin \
You'll notice the admin making fun of you with his meme but also a sql fail at the bottom of the page 

<p align="center">
  <img src="https://user-images.githubusercontent.com/26023804/110697351-8c3cec80-81ec-11eb-91cb-efc78e9277b2.png">
</p>


So if we read the sql line we just have to comment all after **where username = 'admin'** We can acheive that by using as username **admin'--**
Then put a random password and you'll get the flag
