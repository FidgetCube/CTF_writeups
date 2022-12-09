# Mission Hotel- H4 StegSnow (Steganography) 

## Resources

The file size for this challenge was over 70MB and therefore is too large to be uploaded here.

## Solution

Download the image and run file which shows it as a valid .jpg and over 72 MB in size.

<p align="center"><img src="_images/size.png"></p>

Lets find out what is making the image this size. Open it in a hex editor and search for the header (0xFFD8) and footer (0xFFD9) to see if there is any extra data out of place.

<p align="center"><img src="_images/hex.png"></p>

Time to cut that extra data out and save it into a separate file, then we can try and identify what it is and what to do with it. The extra data turned out to be over 70MB of these weird number sequences repeated.

>(1.973694276711756856e+03+6.051639915029231815e+03j), (1.449012052875320842e+04-9.359865272916873437e+03j), 
>(-3.963687854299552782e+03-1.579055054557548829e+03j), (-1.595380755651327718e+02+8.798302406418617466e+03j), 
>(6.669960222240782969e+03-6.114536070708731131e+03j), (-1.497707556949169430e+03-5.865963245464587089e+03j), 
>(-2.394255645262285270e+03+9.393607533138980216e+03j), (-1.813278181627972117e+03+8.427070015803757997e+03j), 
>(6.120954966416011302e+03+2.741969898388250840e+03j), (6.426078877700606427e+02+1.338965982282841196e+02j), 
>(-8.814912071222021041e+03-2.776788579671653224e+03j), (-2.760585235990283309e+03-1.955541728425359224e+03j), 
>(8.803680230064711623e+02-4.029748541614612805e+02j), (-3.195501919189532600e+03-6.725542061819614901e+03j), 
>(2.127361234349085407e+03+4.407263279901763781e+03j), (-2.639510940775000563e+03+2.500663513278394021e+03j), 
>(1.348690182249325699e+04-1.263048984730932716e+03j), (-1.687968172076358769e+03-1.968869455553277703e+03j), 
>(-2.008537456156048620e+03-6.094603101331699690e+01j), (-4.228876299366038438e+03-3.260336606184530865e+03j), 
>(1.257077511100539141e+03-2.771806447551471706e+02j), (2.900101521775442961e+03+2.288139008812128395e+03j), 
>(-2.246784516619854003e+03+1.494979014498743027e+03j), (2.643530360989742576e+02-1.703736466431772214e+03j),

A little googling suggests these are complex numbers and require a Fourier Transform to be conducted in order to process these numbers as an image. I had a friend share his [python code here]() that conducted the transform
