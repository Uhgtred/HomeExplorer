#include <Servo.h>

int ServoXPin = 2;
int ServoZPin = 3;
int RMotorFPin = 10;
int RMotorRPin = 11;
int LMotorFPin = 12;
int LMotorRPin = 13;
int MotorEnablePin = 26;

String stringData;

Servo XServo;
Servo ZServo;
unsigned int servoStart;

void setup() {
    Serial.begin(9600);
    Serial.setTimeout(50);
    XServo.attach(ServoXPin);
    ZServo.attach(ServoZPin);
    pinMode(LMotorFPin, OUTPUT);
    pinMode(LMotorRPin, OUTPUT);
    pinMode(RMotorFPin, OUTPUT);
    pinMode(RMotorRPin, OUTPUT);
    pinMode(MotorEnablePin, OUTPUT);
    digitalWrite(MotorEnablePin, HIGH);
    XServo.write(90);
}

void loop() {
    stringData = Serial.readString(); //"TEST,TEST2,TEST3"; Testing-line
    /*Setting the motor-pins low in each iteration. If something gets stock or communication breaks robot will stop!*/
    digitalWrite(LMotorFPin, LOW);
    digitalWrite(LMotorRPin, LOW);
    digitalWrite(RMotorFPin, LOW);
    digitalWrite(RMotorRPin, LOW);
    if (stringData.length() != 0){
    String *arrayData = ToStringArray(stringData);
    Serial.println(arrayData[0] + arrayData[1]);
    MotorControl(arrayData);
    ServoControl(arrayData);
    delete[] arrayData;
    }
    delay(50);
}

String *ToStringArray(String data){
    /*Making array of comma-separated string!*/
    /*Counting the number of separators to define array-length*/
    char separator;
    separator = ','; 
    int numberOfSeparators = 0;
    for (int i=0; i <= data.length() - 1; i++){
        if  (data[i] == separator){
            numberOfSeparators++;
        }
    }
    /*Defining Array-length and splitting the string into substrings which are bing stored in the array!*/
    String *newData = new String[numberOfSeparators + 1];
    int lastPosition = 0;
    int counter = 0;
    for (int i=0; i <= data.length() - 1; i++){
        // if a separator has been found, the string will be taken from last separator-position to the new position
        if (data[i] == separator){
            newData[counter] = data.substring(lastPosition, i);
            counter++;
            lastPosition = i;
        }
    }
    return newData;
}

void MotorControl(String *arrayData){
    /*Sending PWM-signals to the motor-controllers*/
    int RMotorValue = 0;
    int LMotorValue = 0;
    //reading the data from array which is being provided through the serial-connection
    RMotorValue = arrayData[0].toInt();
    LMotorValue = arrayData[2].toInt();
    //data[1] is bool and decides if RMotor is turning clockwise or counterclockwise
    if (arrayData[1].toInt() == 1){
    analogWrite(RMotorRPin, RMotorValue);
    //Serial.println(RMotorValue);
    }
    else{
    analogWrite(RMotorFPin, RMotorValue);
    //Serial.println(RMotorValue);
    }
    //data[3] is bool and decides if LMotor is turning clockwise or counterclockwise
    if (arrayData[3].toInt() == 1){
    analogWrite(LMotorRPin, LMotorValue);
    //Serial.println(LMotorValue);
    }
    else{
    analogWrite(LMotorFPin, LMotorValue);
    //Serial.println(LMotorValue);
    }
}

void ServoControl(String *arrayData) {
    /*Moving servos with the help of a library which talks to the servos through PWM*/
    //Setting the values from array which is being provided through the serial-connection
    int RStickXValuePos = arrayData[4].toInt();
    int RStickXValueNeg = arrayData[5].toInt();
    int RStickYValuePos = arrayData[6].toInt();
    int RStickYValueNeg = arrayData[7].toInt();
    //XServo.writeMicroseconds(1500);
    //fitting the values from 0-255 to 0-180°
    RStickXValuePos = map(RStickXValuePos, 0, 254, 90, 180);
    RStickXValueNeg = map(RStickXValueNeg, 0, 255, 90, 0);
    //Turning the servos
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
