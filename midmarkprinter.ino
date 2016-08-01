#include <SoftwareSerial.h>

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
