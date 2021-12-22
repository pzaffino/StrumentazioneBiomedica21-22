/**
 * Demonstration of PAJ7620 Gesture Recogniser module
 */

// INCLUDES
// Arduino Wire library is for communicating with any I2C device
#include <Wire.h>
// PAJ7620 library, based on datasheet as described at 
// https://www.epsglobal.com/Media-Library/EPSGlobal/Products/files/pixart/PAJ7620F2.pdf?ext=.pdf
#include "src/PAJ7620/paj7620.h"

void setup() {
  // Initialise serial connection to display results
	Serial.begin(9600);

  // Initialise the sensor
  int error = paj7620Init();
	if(error) {
    //Serial.print(F("Initialisation error code: "));
    //Serial.println(error);
	}
	else {
		//Serial.println(F("Ready!"));
	}
}

void loop() {
  // Create a variable to hold the value of any gesture recognised
	byte gesture;
  // Error variable holds any error code
	int error;
  // Read Reg 0x43 of Bank 0 to get result of any recognised gesture, and store in 'gesture' variable
	error = paj7620ReadReg(0x43, 1, &gesture);
 
	if(!error) {
		switch (gesture) {
			case GES_RIGHT_FLAG:
			  Serial.println(F("Right"));          
				break;
			case GES_LEFT_FLAG: 
				Serial.println(F("Left"));         
				break;
			case GES_UP_FLAG:
				Serial.println(F("Up"));        
				break;
			case GES_DOWN_FLAG:
				Serial.println(F("Down"));         
				break;
			case GES_FORWARD_FLAG:
				Serial.println(F("Forward"));
				break;
			case GES_BACKWARD_FLAG:		  
				Serial.println(F("Backward"));
				break;
      // Library also defines GES_CLOCKWISE_FLAG GES_COUNT_CLOCKWISE_FLAG and GES_WAVE_FLAG, but I found these unreliable
			default:
				break;
		}
	}
 else {
    Serial.print(F("Error code: "));
    Serial.println(error);
 }
  // Introduce small delay before next polling the sensor 
  delay(100);
}
