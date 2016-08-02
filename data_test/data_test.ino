#include <SoftwareSerial.h>

byte b = 0x00;
int len = 0;
const byte END_OF_PRINTOUT = 0xff;
const byte CRLF[] = {0x0d, 0x0a};

void setup() {
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
}

void loop() {
    if (b == 0 && len == 1) {
        Serial.print("Start of test data set...\r\n");
        Serial.print("End of printout code...\r\n");
        Serial.write(END_OF_PRINTOUT);
        Serial.end();
        Serial.begin(9600);
        delay(100);
        Serial.write(END_OF_PRINTOUT);
        delay(100);
        Serial.write(CRLF, 2);
        delay(100);
        Serial.write(CRLF, 2);
        delay(100);
    }

    byte validBuffer[len + 2];
    byte invalidBuffer[len + 2];
    
    for (int i = 0; i < len; i++) {
        validBuffer[i] = b;
        invalidBuffer[i] = b + 0x80;
        b++;
        if (b == CRLF[0] || b == CRLF[1])
          b++;
        if (b > 0x7f)
            b = 0x00;
    }
    validBuffer[len + 1] = CRLF[0];
    validBuffer[len + 2] = CRLF[1];
    invalidBuffer[len + 1] = CRLF[0];
    invalidBuffer[len + 2] = CRLF[1];

    len++;
    if (len > 30)
        len = 1;
    Serial.print("GOOD");
    Serial.write(validBuffer, len + 2);
    Serial.flush();
    Serial.print("BAD\r\n");
    Serial.write(invalidBuffer, len + 2);
    Serial.flush();
    delay(100);
}
