# Trick or treat (programming) 

## Description

200 points  
A user on Ghost Town created a game that he claims no one can beat. Check out the game and find the flag hidden inside. 
Submit the flag as: flag{flag-goes-here}.

## Resources

[Provided game files](https://github.com/FidgetCube/CTF_writeups/blob/main/2021-DEADFACE-CTF/TrickOrTreat(programming)/game.zip)

## Solution

This was one of my favourite challenges in all CTFs i have done. It was quite simple but really enjoyable because of the many ways you could choose to exploit the game or just steal the flag.

The first step was to run the game and see what it was all about. It was a cool little game where the object was to move the cvharacter and avoid the grim reapers that ran down the screen. Each time you successfuly dodged one, your "dodged" score went up by 1 and the next grim reaper sped up. If the grim reaper touched you then you died and the game ended.

So now it's time to pick the code apart. We assume that the flag is printed once you reach a certain score so we go looking for that part in the code and quickly realise the code is mildly obfuscated mostly just by poor variable names. 

The simplest way to beat this but the least fun was to find the section where the game tests if you have a high enough score and prints a flag, and just call the function to print the flag in main when the game starts.

The fun way to tackle this was to modify game paramters to cheat the game. For instance you could removed the line that tested for a collison and so you effectively had god mode and couldn't die.

I was impatient so at first i sped the grim reapers up so that 100 came down in about 2 seconds so it was over fast, then i decided to just award 100 points for each successful dodge so that you only had to dodge 1 enemy to beat the game.


<p align="center"><img src="_images/1challengeDesc.png"></p>

<p align="center"><img src="_images/2nc.png"></p>

<p align="center"><img src="_images/3dcode.png"></p>

<p align="center"><img src="_images/5solve.png"></p>
