#include <Servo.h>

//int ServoXPin = 6;
//int ServoZpin = 5;
int RMotorFPin = 3;
int RMotorRPin = 9;
int LMotorFPin = 10;
int LMotorRPin = 11;

String stringData;

//Servo XServo; 
//Servo ZServo;
unsigned int servoStart;

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(50);
  //pinMode(ServoXPin, OUTPUT);
  /*
  XServo.attach(ServoXPin);
  ZServo.attach(ServoZpin);
  */
  pinMode(LMotorFPin, OUTPUT);
  pinMode(LMotorRPin, OUTPUT);
  pinMode(RMotorFPin, OUTPUT);
  pinMode(RMotorRPin, OUTPUT);
  //XServo.write(90);
}

void loop() {
  stringData = Serial.readString();
  digitalWrite(LMotorFPin, LOW);
  digitalWrite(LMotorRPin, LOW);
  digitalWrite(RMotorFPin, LOW);
  digitalWrite(RMotorRPin, LOW);
  if (stringData.length() != 0){
    char charData[(stringData.length())];
    stringData.toCharArray(charData, stringData.length());
    MotorControl(charData);
    //ServoControl(charData);
  }
  delay(50);
}

void MotorControl(char charData[]){
  int RMotorValue = 0;
  int LMotorValue = 0;
  RMotorValue = (int(charData[0]) - 48) * 100 + (int(charData[1]) - 48) * 10 + (int(charData[2]) - 48);
  LMotorValue = (int(charData[4]) - 48) * 100 + (int(charData[5]) - 48) * 10 + (int(charData[6]) - 48);
  if ((int(charData[3]) - 48) == 1){ //data[3] is bool and decides if RMotor is turning backward or forward
    analogWrite(RMotorRPin, RMotorValue);
    //Serial.println(RMotorValue);
  }
  else{
    analogWrite(RMotorFPin, RMotorValue);
    //Serial.println(RMotorValue);
  }
  if ((int(charData[7]) - 48) == 1){ //data[7] is bool and decides if LMotor is turning backward or forward
    analogWrite(LMotorRPin, LMotorValue);
    //Serial.println(LMotorValue);
  }
  else{
    analogWrite(LMotorFPin, LMotorValue);
    //Serial.println(LMotorValue);
  }
}
/*
void ServoControl(char charData[]) {
  int RStickXValuePos = (int(charData[8]) - 48) * 100 + (int(charData[9]) - 48) * 10 + (int(charData[10]) - 48);
  int RStickXValueNeg = (int(charData[11]) - 48) * 100 + (int(charData[12]) - 48) * 10 + (int(charData[13]) - 48);
  int RStickYValuePos = (int(charData[14]) - 48) * 100 + (int(charData[15]) - 48) * 10 + (int(charData[16]) - 48);
  int RStickYValueNeg = (int(charData[17]) - 48) * 100 + (int(charData[18]) - 48) * 10 + (int(charData[19]) - 48);
  //XServo.writeMicroseconds(1500);
  RStickXValuePos = map(RStickXValuePos, 0, 254, 90, 180);
  RStickXValueNeg = map(RStickXValueNeg, 0, 255, 90, 0);

  if (RStickXValuePos > 90){
     XServo.write(RStickXValuePos);
  }
  else if (RStickXValueNeg < 90){
    XServo.write(RStickXValueNeg);
  }
  else{
    XServo.write(90);
  }             
}*/
