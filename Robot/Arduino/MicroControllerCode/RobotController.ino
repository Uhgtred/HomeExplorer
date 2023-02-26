#include <Servo.h>

int ServoXPin = 2;
int ServoZpin = 3;
int RMotorFPin = 6;
int RMotorRPin = 7;
int LMotorFPin = 8;
int LMotorRPin = 9;
int Battery0Pin = 35;
int Battery1Pin = 37;
int Battery2Pin = 39;
int Battery3Pin = 41;
int Battery4Pin = 43;
int Battery5Pin = 45;
int Battery6Pin = 47;
int Battery7Pin = 49;
int Battery8Pin = 51;
int Battery9Pin = 53;

String stringData;

Servo XServo; 
Servo ZServo;
unsigned int servoStart;

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(50);
  XServo.attach(ServoXPin);
  ZServo.attach(ServoZpin);
  pinMode(LMotorFPin, OUTPUT);
  pinMode(LMotorRPin, OUTPUT);
  pinMode(RMotorFPin, OUTPUT);
  pinMode(RMotorRPin, OUTPUT);
  XServo.write(90);
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
    ServoControl(charData);
  }
}

void MotorControl(char charData[]){
  int RMotorValue = 0;
  int LMotorValue = 0;
  RMotorValue = (int(charData[0]) - 48) * 100 + (int(charData[1]) - 48) * 10 + (int(charData[2]) - 48);
  LMotorValue = (int(charData[4]) - 48) * 100 + (int(charData[5]) - 48) * 10 + (int(charData[6]) - 48);
  if ((int(charData[3]) - 48) == 1){ //data[3] is bool and decides if RMotor is turning backward or forward
    analogWrite(RMotorRPin, RMotorValue);
  }
  else{
    analogWrite(RMotorFPin, RMotorValue);
  }
  if ((int(charData[7]) - 48) == 1){ //data[7] is bool and decides if LMotor is turning backward or forward
    analogWrite(LMotorRPin, LMotorValue);
  }
  else{
    analogWrite(LMotorFPin, LMotorValue);
  }
}

void ServoControl(char charData[]) {
  int RStickXValuePos = (int(charData[8]) - 48) * 100 + (int(charData[9]) - 48) * 10 + (int(charData[10]) - 48);
  int RStickXValueNeg = (int(charData[11]) - 48) * 100 + (int(charData[12]) - 48) * 10 + (int(charData[13]) - 48);
  int RStickYValuePos = (int(charData[14]) - 48) * 100 + (int(charData[15]) - 48) * 10 + (int(charData[16]) - 48);
  int RStickYValueNeg = (int(charData[17]) - 48) * 100 + (int(charData[18]) - 48) * 10 + (int(charData[19]) - 48);

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
}

void BatteryStatus(){
  digitalWrite(Battery0Pin, HIGH);
}

void voltageMeasurement() {
  float voltageValue;
  int analogValue = analogRead(A0);
  if (analogValue != 0){
    float tempValue = (analogValue * 5) / 1024;
    voltageValue = tempValue / 0.909091; //(100000 / (10000 + 100000))
    Serial.println(voltageValue);
  }
  else{
    voltageValue = 0;
  }
}
