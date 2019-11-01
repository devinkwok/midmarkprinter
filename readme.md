Arduino-based printer emulator for sterilizer
=============================================

An emulator for the Epson M160 dot matrix printer attachment for the Midmark M11 Sterilizer (autoclave). Developed for ASK Dental Clinic to produce digital backups of sterilization records.

The sterilizer sends data as ASCII characters on a single standard serial line (LSB first) at a baud rate of 9600. The following pinout was reverse engineered from the serial port, which normally outputs to the physical tape printer.

Usage instructions
------------------
* Download and install Arduino IDE at: https://www.arduino.cc/en/Main/Software
* Open midmarkprinter.ino in Arduino IDE.
* Connect Arduino board to computer using USB.
* Click "Upload" button (arrow) at top left.
* Connect Arduino pins: pin 4 outputs constant voltage to pin 5 on sterilizer, pin 10 receives serial data from pin 4 on sterilizer, ground pin to either pin 1 or 8 on sterilizer.
* Run sterilizer-printer.exe on computer.

Sterilizer printer interface pinout
-----------------------------------
0. GROUND (rightmost)
1. POWER MOTOR (4.8V)
2. POWER IC (4.8V)
3. REED SWITCH (GROUND)
4. DATA 9600 BAUD (4.5V PULL UP)
5. FEED PAPER (INPUT 5V TO SEND PRINT DATA)
6. REED SWITCH (4.5V PULL UP)
7. UNKNOWN (FROM PRINTER?)

Arduino pinout
--------------
* 4 - Fixed output to feed paper (4.8V)
* 10 - serial data in
* GROUND to ground
* POWER to power

Sample output
-------------
```
------------------------
  Midmark M11 - v1.0.4
   Total Cycles: 2194

  ____________________
      Sterilizer ID

  ____________________
        Operator

 05 / 05 / 2017  13 : 47
 mm / dd / yyyy  hh : mm

  BEGIN UNWRAPPED CYCLE
  Temp:  270 Degrees F
  Time:    3 Minutes
   Dry:   35 Minutes

     FILLING CHAMBER

         HEATING
  mm:ss  Degrees   PSI
   0:00   68.0 F   0.1
```
