# Operation Orchid (Forensics 400 points) 

## Description

Download this disk image and find the flag. Note: if you are using the webshell, download and extract the disk image into /tmp not your home directory.

    Download compressed disk image

*No hints*

## Resources

[Disk Image download](https://artifacts.picoctf.net/c/239/disk.flag.img.gz)

## Solution

Download and extract the provided disk image.

Load the .img image file into autopsy by creating a new case. Browse volume 3 and click on "file analysis" at the top of the screen.

Browsr the folder structure looking for files of value and under /root there is a file called flag.txt which has been deleted, flag.txt.enc which contains the encrypted flag. Also of note and probably the best reason to use Autopsy here is there is hidden file displayed called *.ash_history* which contains the command history. You can see the commands used to create the flag and delete the file but most importantly is the openssl command used to encrypt the flag which also shows the password used.

>openssl aes256 -salt -in flag.txt -out flag.txt.enc -k unbreakablepassword1234567

<p align="center"><img src="_images/1.png"></p>

export flag.txt.enc and save it your local host.

<p align="center"><img src="_images/3.png"></p>

Decrypt the flag using the openssl command by adding the decrypt argument *-d*, ensure you pass the encrypted flag as the input *-in* and stipulate a text file as the output *-out* to write the decrypted flag to. Leave the password form the original command as this is required to decrypt the flag.

>openssl aes256 -d -in flag.txt.enc -out flag.txt -k unbreakablepassword1234567

<p align="center"><img src="_images/2.png"></p>

Flag is 

# picoCTF{h4un71ng_p457_c512004e}