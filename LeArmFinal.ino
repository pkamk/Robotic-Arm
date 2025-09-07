#include <xArmServoController.h>
#include <SoftwareSerial.h>
#include <SD.h>
#include <SPI.h>

// To use SoftwareSerial:
// 1. Uncomment include statement above and following block.
// 2. Update xArmServoController with mySerial.
// 3. Change Serial1.begin to mySerial.begin.
// 4. rxPin 2 and txPin 3

#define rxPin 2
#define txPin 3
#define chipSelectSD 10

File robotArmDataLog;

SoftwareSerial mySerial = SoftwareSerial(rxPin, txPin);


xArmServoController myArm = xArmServoController(LeArm, mySerial);

void setup() {
  SD.begin(10);
  robotArmDataLog = SD.open("datalog.txt", FILE_WRITE);
  mySerial.begin(9600);
  Serial.begin(115200);
  Serial.setTimeout(1);
  /*
  // xArm servo positions
   xArmServo home[] = {{1, 500},M
                      {2, 500},
                      {3, 500},
                      {4, 500},
                      {5, 500},
                      {6, 500}};
  xArmServo bow[] = {{1, 650},
                     {3, 130},
                     {4, 845},
                     {5, 650}};
                     */
 
  // LeArm servo positions. To use:
  // 1. Comment out above xArmServo definitions above.
  // 2. Change xArmServoController mode to LeArm.
  // 3. Uncomment following block.
  
  /*xArmServo home[] = {{1, 1500},
                      {2, 1500},
                      {3, 1500},
                      {4, 1500},
                      {5, 1500},
                      {6, 1500}};
  xArmServo bow[] = {{1, 2365},
                     {3, 520},
                     {4, 650},
                     {5, 1035}};
   xArmServo swingRight[] = {{3, 1000},
                            {4, 850},
                            {5, 1200},
                            {6, 2000}};                            
    

  myArm.setPosition(home, 6, 1000, true);
  delay(1000);
  myArm.setPosition(bow, 4, 3000, true);
  delay(1000);
  myArm.setPosition(home, 6);*/

  // Your setup here.
}

void loop() {
  while (!Serial.available());
  //char buf[200];
  //Serial.readBytes(buf,200);
  String angleValue = Serial.readStringUntil("|");
  char *buf = angleValue.c_str();
  char *angleValueString7 = strtok(buf, ",");
  char *angleValueString6 = strtok(NULL, ",");
  char *angleValueString5 = strtok(NULL, ",");
  char *angleValueString4 = strtok(NULL, ",");
  char *angleValueString3 = strtok(NULL, ",");
  char *angleValueString2 = strtok(NULL, ",");
  char *angleValueString1 = strtok(NULL, ",");
  //char *trem = strtok(NULL, ",");

  String p1 = "," ;
  robotArmDataLog.println("in:" + String(angleValueString6) + p1 + String(angleValueString5) + p1 + String(angleValueString4) + p1 + String(angleValueString3) + p1 + String(angleValueString2) + p1 + String(angleValueString1));
  // 1
  robotArmDataLog.flush();
  if (angleValueString1 != NULL) {

    int angleValue6 = atoi(angleValueString6);
    int angleValue5 = atoi(angleValueString5);
    int angleValue4 = atoi(angleValueString4);
    int angleValue3 = atoi(angleValueString3);
    int angleValue2 = atoi(angleValueString2);
    int angleValue1 = atoi(angleValueString1);

    if (robotArmDataLog) {
    robotArmDataLog.println(angleValue6 + p1 + angleValue5 + p1 + angleValue4 + p1 + angleValue3 + p1 + angleValue2 + p1 + angleValue1);
    robotArmDataLog.flush();
    } 
  
    xArmServo home[] = {{1, angleValue1},
                        {2, angleValue2},
                        {3, angleValue3},
                        {4, angleValue4},
                        {5, angleValue5},
                        {6, angleValue6}};
    /*xArmServo bow[] = {{1, 2365},
                       {3, 520},
                       {4, 650},
                       {5, 1035}};
                       
    xArmServo swingRight[] = {{3, 1000},
                              {4, 850},
                              {5, 1200},
                              {6, 2000}};  
    xArmServo swingFurther[] = {{3, 1200},
                              {4, 1250},
                              {5, 1400},
                              {6, 2400}};*/                                                                 
      
  
    myArm.setPosition(home, 6, 1, true);
    delay(1);
    //Serial.println(String(angleValue6)+"\n");
    //Serial.flush();
    /*myArm.setPosition(bow, 4, 3000, true);
    delay(1000);
    myArm.setPosition(swingRight, 4, 1000, true);
    delay(1000);
    myArm.setPosition(swingFurther, 4, 1000, true);
    delay(1000);*/
    }
}
