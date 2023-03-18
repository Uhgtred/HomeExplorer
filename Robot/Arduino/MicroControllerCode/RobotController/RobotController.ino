#include <Servo.h>

/*
Declaring and defining Pins (could also be data-type short to safe some memory)
*/
const unsigned short ServoXPin = 2;
const unsigned short ServoZPin = 3;
const unsigned short RMotorFPin = 10;
const unsigned short RMotorRPin = 11;
const unsigned short LMotorFPin = 12;
const unsigned short LMotorRPin = 13;
const unsigned short MotorEnablePin = 26;

const unsigned short maxMessageSize = 50;
char serialData[maxMessageSize];

Servo XServo;
Servo ZServo;

void setup() {
    //Setting up serial parameters
    Serial.begin(9600);
    //Setting up Servos
    XServo.attach(ServoXPin);
    ZServo.attach(ServoZPin);
    //Setting up Pins for Motor-control
    pinMode(LMotorFPin, OUTPUT);
    pinMode(LMotorRPin, OUTPUT);
    pinMode(RMotorFPin, OUTPUT);
    pinMode(RMotorRPin, OUTPUT);
    pinMode(MotorEnablePin, OUTPUT);
    //Enabling motors by setting "enable"-pin on motor-controller-board high (5V)
    digitalWrite(MotorEnablePin, HIGH);
    //Making sure Servos are in default-position
    XServo.write(90);
    //ZServo.write(90);
}

void loop() {
    int counter = 0;
    while (Serial.available() > 0){
      char readByte = Serial.read();
      if (readByte != '&' and counter <= maxMessageSize){
        serialData[counter] = readByte;
        counter++;
      }
      else{
        break;
      }
    }
    //Setting the motor-pins low in each iteration. If something gets stock or communication breaks robot will stop!
    digitalWrite(LMotorFPin, LOW);
    digitalWrite(LMotorRPin, LOW);
    digitalWrite(RMotorFPin, LOW);
    digitalWrite(RMotorRPin, LOW);
   if (serialData.length() != 0){
        int* arrayData = ToStringArray(serialData);  // splitting the received string into an array
        Serial.println(arrayData[0] + arrayData[1]);  // debugging-line
        //Sending transformed data to motors and servos
        MotorControl(arrayData);
        ServoControl(arrayData);
        delete[] arrayData;  // deleting the array-pointer to release memory
   }
   delay(50);
}

String *ToStringArray(char data){
    /*
    Making array of comma-separated string!
    */
    //Counting the number of separators to define array-length
    char separator;
    separator = ','; 
    short numberOfSeparators = 0;
    for (short i=0; i <= data.length(); i++){
        if  (data[i] == separator){
            numberOfSeparators++;
        }
    }
    //Defining Array-length and splitting the string into substrings which are being stored in the array!
    int *newData = new String[numberOfSeparators + 1];
    //int lastPosition = 0;
    short counter = 0;
    String tempString;
    for (short i=0; i <= data.length(); i++){
        //If a separator has been found, the string will be taken from last separator-position to the new position
        //*new version*: adding characters to a string until there is a ',' beingread. then converting string to int and adding it to int-array
        tempString += data[i];
        if (data[i] == separator or i==data.length()){
            newData[counter] =  tempString.toInt();     //data.substring(lastPosition, i); //old version
            counter++;
            tempString = "";
            //lastPosition = i + 1;  //the +1 removes the comma from the next string // old version
        }
    }
    return newData;
}

void MotorControl(int *arrayData){
    /*
    Sending PWM-signals to the motor-controllers
    */
    int RMotorValue = 0;
    int LMotorValue = 0;
    //reading the data from array which is being provided through the serial-connection
    RMotorValue = arrayData[0];
    LMotorValue = arrayData[2];
//    Serial.println("RMotor: "+ String(RMotorValue) + " LMotor: " + String(LMotorValue));  // debugging-line
//    Serial.println("ARRAYDATA: " + arrayData[0] + arrayData[1] + arrayData[2] + arrayData[3]);  // debugging-line
    //data[1] is bool and decides if RMotor is turning clockwise or counterclockwise
    if (arrayData[1] == 1){
        analogWrite(RMotorRPin, RMotorValue);
//        Serial.println(RMotorValue);  // debugging-line
    }
    else{
        analogWrite(RMotorFPin, RMotorValue);
//        Serial.println(RMotorValue);  // debugging-line
    }
    //data[3] is bool and decides if LMotor is turning clockwise or counterclockwise
    if (arrayData[3] == 1){
        analogWrite(LMotorRPin, LMotorValue);
//        Serial.println(LMotorValue);  // debugging-line
    }
    else{
        analogWrite(LMotorFPin, LMotorValue);
//        Serial.println(LMotorValue);  // debugging-line
    }
}

void ServoControl(int *arrayData) {
    /*
    Moving servos with the help of a library which talks to the servos through PWM
    */
    //Setting the values from array which is being provided through the serial-connection
    int RStickXValuePos = arrayData[4];
    int RStickXValueNeg = arrayData[5];
    int RStickYValuePos = arrayData[6];
    int RStickYValueNeg = arrayData[7];
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
