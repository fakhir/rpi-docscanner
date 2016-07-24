# Raspberry Pi Scan-to-Dropbox Utility for HP MFP Scanners
A Raspberry Pi based scan-to-dropbox utility with a Blynk UI. Uses an HP MFP printer for scanning documents.

# Setting up your phone
Install the "Blynk" app on your phone. If you can't find the app in the store, then try using
the direct link from the following page:
http://docs.blynk.cc/

## Setting up the Raspberry Pi
Install the following packages on your Raspberry Pi:

```
$ sudo apt-get install python-pillow
$ sudo apt-get install python-numpy
```

Install NodeJS and Blynk library on the Raspberry Pi by following steps 1 here:
http://www.instructables.com/id/Blynk-JavaScript-in-20-minutes-Raspberry-Pi-Edison

## Running the docscanner
First manually run the docscanner and check everything works fine:
```
$ cd rpi-docscanner
$ ./blynk-docscanner.js
```
