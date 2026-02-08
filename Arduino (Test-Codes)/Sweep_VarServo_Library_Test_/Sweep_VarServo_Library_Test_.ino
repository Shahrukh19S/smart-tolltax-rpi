/*
  Sweep
  by BARRAGAN <http://barraganstudio.com> 
  Adapted by Philip van Allen <philvanallen.com> for the VarSpeedServo.h library (October 2013)
  This example code is in the public domain
  
  Sweep a servo back and forth from 0-180 degrees, 180-0 degrees
  Uses the wait feature of the 2013 version of VarSpeedServo to stop the code until the servo finishes moving
  
  Note that servos usually require more power than is available from the USB port - use an external power supply!
*/

#include <VarSpeedServo.h> 
 
VarSpeedServo myservo;  // create servo object to control a servo 
                        // a maximum of eight servo objects can be created 
 
const int servoPin = 6; // the digital pin used for the servo
 
void setup() { 
  myservo.attach(servoPin);  // attaches the servo on pin 9 to the servo object
  myservo.write(0,20,true); // set the intial position of the servo, as fast as possible, wait until done
} 

void loop() {
  //myservo.write(90,20,true);        // move the barrier servo to 90, max speed, wait until done
  myservo.write(45,20,true);        // move the barcode scanner servo to 40, max speed, wait until done
  delay(60);                                    // write(degrees 0-180, speed 1-255, wait to complete true-false)
  myservo.write(0,20,true);           // move the servo to 180, slow speed, wait until done
  delay(60);
} 
