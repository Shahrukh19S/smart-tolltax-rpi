#include <NewPing.h>
#include <VarSpeedServo.h> 
#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define RST_PIN 9

MFRC522 mfrc522(SS_PIN, RST_PIN);   // Create MFRC522 instance.

VarSpeedServo rotScanner;  // create servo object to control a servo 
                         // a maximum of eight servo objects can be created 
VarSpeedServo barrierServo;
 
#define TRIGGER_PIN  8  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN     7  // Arduino pin tied to echo pin on the ultrasonic sensor.
#define MAX_DISTANCE 30 // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.

NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE); // NewPing setup of pins and maximum distance.

const int ConvMotor1 = 2;
const int ConvMotor2 = 3;
const int red_LED = 5;
const int Green_LED = 4;
const int scanner = 6;
const int barrier = 9;
const int RFID_pin = A0;

int distance = 0;
boolean isRFID = true;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);   // Initiate a serial communication
  SPI.begin();      // Initiate  SPI bus
  mfrc522.PCD_Init();   // Initiate MFRC522
  pinMode(ConvMotor1,OUTPUT);
  pinMode(ConvMotor2,OUTPUT);
  pinMode(red_LED,OUTPUT);
  pinMode(Green_LED,OUTPUT);
  pinMode(RFID_pin, INPUT_PULLUP); 
  rotScanner.attach(scanner);  // attaches the servo on pin 9 to the servo object
  rotScanner.write(0,20,false); // set the intial position of the servo, as fast as possible, run in background
  barrierServo.attach(barrier);  // attaches the servo on pin 9 to the servo object
  barrierServo.write(0,50,false);  // set the intial position of the servo, as fast as possible, wait until done

}

void loop() {
  // put your main code here, to run repeatedly:
  while(!Serial.available()){
    //run conveyer,detect objects and rotate Scanner as long as Rpi doesn't scans the barcode.
   distance = getdistance();
   int UseRFID = digitalRead(RFID_pin);
   digitalWrite(red_LED,HIGH);
   digitalWrite(Green_LED,LOW);
   if((distance>0 && distance <=20) && (UseRFID == HIGH)){ //Manual button for RFID is not pushed, therefore, continue with Barcode Scanning.
    //Serial.println("running in auto");
    delay(500);
    stop();
    rotatebarScan();
    delay(1000);
    }
  else if((distance>0 && distance <=20) && (UseRFID == LOW)){
      delay(500);
      stop();
      //Serial.println("running in manual");
      detectRFIDOwner();
      delay(400);
  }
  else{
    forward();
    }   
  }
  if(Serial.available()>0){
   int myval=Serial.read();
   if(myval == '1'){
    barrierOpen();
   }
   barrierClose();
  }
}

void forward()
{  
  digitalWrite(ConvMotor1,HIGH);
  digitalWrite(ConvMotor2,LOW);
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

void rotatebarScan(){
  rotScanner.write(45,20,true);         // move the servo to 180, fast speed, wait until done
  delay(60);
  rotScanner.write(0,20,true);            // move the servo to 180, slow speed, wait until done
  delay(60);
  
  
}

void barrierOpen(){
  barrierServo.write(90,50,false);        // move the servo to 180, fast speed, run background
  delay(60);
  digitalWrite(red_LED, LOW);
  digitalWrite(Green_LED, HIGH);
  forward();
  delay(6000);
}

void barrierClose(){
  barrierServo.write(0,50,false);
  digitalWrite(red_LED, HIGH);
  digitalWrite(Green_LED, LOW);
}

int detectRFIDOwner(){
  // Look for new cards
  if ( ! mfrc522.PICC_IsNewCardPresent()) 
  {
    return;
  }
  // Select one of the cards
  if ( ! mfrc522.PICC_ReadCardSerial()) 
  {
    return;
  }
  String content= "";
  //byte letter;
  for (byte i = 0; i < mfrc522.uid.size; i++) 
  {
     //Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
     //Serial.print(mfrc522.uid.uidByte[i], HEX);
     content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
     content.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  content.toUpperCase();
  if (content.substring(1) == "D9 1B FE 7E") //change here the UID of the card/cards that you want to give access
  {
    // Maheen RFID Card detected
    Serial.print("4");
    //Serial.println("Authorized access");
  }
  else if(content.substring(1) == "59 41 40 29"){
    //Areeba RFID Card Detected
    Serial.print("3"); 
  }
  else{
    barrierClose();
    //Serial.println("Acess Denied");
  }
}


