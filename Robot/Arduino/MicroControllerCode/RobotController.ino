//#include <Servo.h>

int ServoXPin = 2;
int ServoZpin = 3;
int RMotorFPin = 10;
int RMotorRPin = 11;
int LMotorFPin = 12;
int LMotorRPin = 13;
int MotorEnablePin = 26;

String stringData;

//Servo XServo; 
//Servo ZServo;
unsigned int servoStart;

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(50);
  //XServo.attach(ServoXPin);
  //ZServo.attach(ServoZpin);
  pinMode(LMotorFPin, OUTPUT);
  pinMode(LMotorRPin, OUTPUT);
  pinMode(RMotorFPin, OUTPUT);
  pinMode(RMotorRPin, OUTPUT);
  pinMode(MotorEnablePin, OUTPUT);
  digitalWrite(MotorEnablePin, HIGH);
  //XServo.write(90);
}

void loop() {
  stringData = Serial.readString();
  digitalWrite(LMotorFPin, LOW);
  digitalWrite(LMotorRPin, LOW);
  digitalWrite(RMotorFPin, LOW);
  digitalWrite(RMotorRPin, LOW);
  if (stringData.length() != 0){
    String *arrayData = ToStringArray(stringData);
    Serial.println(arrayData[0] + arrayData[1]);
    //MotorControl(arrayData);
    //ServoControl(arrayData);
    delete[] arrayData;
  }
  delay(50);
}

String *ToStringArray(String data){
    """Making array of comma-separated string!"""
    char separator;
    separator = ','; 
    int numberOfSeparators = 0;
    for (int i=0; i <= data.length() - 1; i++){
        if  (data[i] == separator){
            numberOfSeparators++;
        }
    }
    String *newData = new String[numberOfSeparators + 1];
    int lastPosition = 0;
    int counter = 0;
    for (int i=0; i <= data.length() - 1; i++){
        if (data[i] == separator){
            newData[counter] = data.substring(lastPosition, i);
            counter++;
            lastPosition = i;
        }
    }
    return newData;
}

void MotorControl(String *arrayData){
  int RMotorValue = 0;
  int LMotorValue = 0;
  RMotorValue = arrayData[0].toInt();// - 48);   //charData[0]) - 48) * 100 + (int(charData[1]) - 48) * 10 + (int(charData[2]) - 48);
  LMotorValue = arrayData[2].toInt(); // - 48) * 100 + (int(charData[5]) - 48) * 10 + (int(charData[6]) - 48);
  if (arrayData[1].toInt() == 1){ //data[3] is bool and decides if RMotor is turning backward or forward
    analogWrite(RMotorRPin, RMotorValue);
    //Serial.println(RMotorValue);
  }
  else{
    analogWrite(RMotorFPin, RMotorValue);
    //Serial.println(RMotorValue);
  }
  if (arrayData[3].toInt() == 1){ //data[7] is bool and decides if LMotor is turning backward or forward
    analogWrite(LMotorRPin, LMotorValue);
    //Serial.println(LMotorValue);
  }
  else{
    analogWrite(LMotorFPin, LMotorValue);
    //Serial.println(LMotorValue);
  }
}
/*
void ServoControl(char charData*) {
  int RStickXValuePos = int(arrayData[4]) - 48);// * 100 + (int(charData[9]) - 48) * 10 + (int(charData[10]) - 48);
  int RStickXValueNeg = int(arrayData[5]) - 48); //* 100 + (int(charData[12]) - 48) * 10 + (int(charData[13]) - 48);
  int RStickYValuePos = int(charData[6]) - 48); //* 100 + (int(charData[15]) - 48) * 10 + (int(charData[16]) - 48);
  int RStickYValueNeg = int(charData[7]) - 48); //* 100 + (int(charData[18]) - 48) * 10 + (int(charData[19]) - 48);
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
