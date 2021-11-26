# Result (misc, Crypto)

## Description

>I really want to know my test result, but unfortunately its additionally protected. I attached the email. Maybe you can help?

## Solution

I downloaded the provided zip file and extracted the email contained inside. Opening the email in Sublime, i can see that the email has a .pdf attachment.
<p align="center"><img src="_images/emailpdf.png"></p>

There is also reference to password protection and the structure of the password. This will form the basis of the wordlist i make a little later.
<p align="center"><img src="_images/emailpassword.png"></p>

Next step was to extract the .pdf file from the email so i copy the block of base64 encoded data and paste it into cyberchef. Adding the "from base64" recipe you can see the .pdf file in the results section. I saved the file to my local machine and tried to open it, where i was met with a password prompt.
<p align="center"><img src="_images/passwordprompt.png"></p>
