#include <SoftwareSerial.h>
/*
 * PINS:
 * 
 * on midmark sterilizer:
 * 0. GROUND (rightmost)
 * 1. POWER MOTOR (4.8V)
 * 2. POWER IC (4.8V)
 * 3. REED SWITCH (GROUND)
 * 4. DATA 9600 BAUD (4.5V PULL UP)
 * 5. FEED PAPER (INPUT 5V TO SEND PRINT DATA)
 * 6. REED SWITCH (4.5V PULL UP)
 * 7. UNKNOWN (FROM PRINTER?)
 * 
 * on arduino:
 * 4 - fixed voltage to pin 5 (feed)
 * 10 - serial data in
 * ground to ground
 * power to power
 */


long BAUD = 9600;
SoftwareSerial mySerial(10, 11); // RX, TX
int voltagePin = 4;              // fixed voltage to device

void setup() {
  pinMode(voltagePin, OUTPUT);
  digitalWrite(voltagePin, HIGH);
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  mySerial.begin(BAUD);

  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
}

void loop() {
  // read any data from serial
  if (mySerial.available())
    Serial.write(mySerial.read());
}
