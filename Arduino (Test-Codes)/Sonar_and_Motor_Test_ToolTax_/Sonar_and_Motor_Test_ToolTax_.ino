
#include <NewPing.h>
#include <VarSpeedServo.h> 
 
VarSpeedServo myservo1;  // create servo object to control a servo 
                         // a maximum of eight servo objects can be created 
VarSpeedServo myservo2;
 
#define TRIGGER_PIN  12  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN     11  // Arduino pin tied to echo pin on the ultrasonic sensor.
#define MAX_DISTANCE 30 // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.

NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE); // NewPing setup of pins and maximum distance.

const int speed = 90;
const int ConvMotor1 = 2;
const int ConvMotor2 = 3;
const int red_LED = 4;
const int Green_LED = 5;
const int rotscanner = 9; // the digital pin used for the first servo
const int barrier = 10; // the digital pin used for the second servo
boolean isBarScan = false;
void setup() {
  // put your setup code here, to run once:
Serial.begin(115200); // Open serial monitor at 115200 baud to see ping results.
pinMode(ConvMotor1,OUTPUT);
pinMode(ConvMotor2,OUTPUT);
pinMode(red_LED,OUTPUT);
pinMode(Green_LED,OUTPUT); 
myservo1.attach(barrier);  // attaches the servo on pin 9 to the servo object
myservo1.write(0,50,false); // set the intial position of the servo, as fast as possible, run in background
myservo2.attach(rotscanner);  // attaches the servo on pin 9 to the servo object
myservo2.write(0,20,false);  // set the intial position of the servo, as fast as possible, wait until done
  
 
}

void loop() {
  // put your main code here, to run repeatedly:
  forward();
  int distance = getdistance();
  Serial.println(distance);
  if(distance>0 && distance <=20){
    isBarScan = true;
    delay(2000);
    stop();
     
    Serial.println("Object Detected");
    
}
  if(isBarScan == true)
  {
    stop();
    isBarScan = false;
    RotatebarScan();
  }
}

void forward()
{  
  digitalWrite(ConvMotor1,HIGH);
  digitalWrite(ConvMotor2,LOW);
  digitalWrite(red_LED,HIGH);
  digitalWrite(Green_LED,LOW);
}

void stop()
{
    digitalWrite(ConvMotor1,LOW);
    digitalWrite(ConvMotor2,LOW);
    digitalWrite(red_LED,HIGH);
    digitalWrite(Green_LED,LOW);
}

long getdistance()
{
  delay(50);
long  distance=sonar.ping_cm();
  return (distance);         //return distance in cm
}

void RotatebarScan(){
  myservo2.write(45,20,true);         // move the servo to 180, fast speed, wait until done
  delay(60);
  myservo2.write(0,20,true);            // move the servo to 180, slow speed, wait until done
  delay(60);
  
}

void BarrierOpen(){
  myservo1.write(90,50,true);        // move the servo to 180, fast speed, run background
}

void BarrierClose(){
  myservo1.write(0,50,true);        // move the servo to 180, fast speed, run background

}

