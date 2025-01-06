#include <Servo.h>
#include <ArduinoJson.h>

/*
Declaring and defining Pins
*/
const unsigned short ServoXPin = 2;
const unsigned short ServoZPin = 3;
const unsigned short RMotorFPin = 10;
const unsigned short RMotorRPin = 11;
const unsigned short LMotorFPin = 12;
const unsigned short LMotorRPin = 13;
const unsigned short MotorEnablePin = 26;

Servo XServo;
Servo ZServo;

/*
Declaring and defining global Variables.
*/
StaticJsonDocument<80> jsonDocument;
struct actorMapDataType {
    String actorName;
    String actorID;
};

void setup() {
    //Setting up serial parameters
    Serial.begin(115200);
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
    ZServo.write(90);
}

void loop() {
    readSerialJson();
    //Sending transformed data to motors and servos
    MotorControl();
    //ServoControl();
    //Serial.println(String(serialByteData[0]) + ' ' + String(serialByteData[2]));
}

int readJsonValue(String key){
    int value = jsonDocument[key];
    return value;
}

void readSerialJson(){
    if (Serial.available()){
        String jsonData = Serial.readStringUntil('&');
        // storing jsonData into global json document
        deserializeJson(jsonDocument, jsonData);
    }
}

void SetMotorsZero(void){
    //Setting the motor-pins low in each iteration. If something gets stuck or communication breaks robot will stop!
    SetLeftMotorsZero();
    SetRightMotorsZero();
}

void SetLeftMotorsZero(void){
    digitalWrite(LMotorFPin, LOW);
    digitalWrite(LMotorRPin, LOW);
}

void SetRightMotorsZero(void){
    digitalWrite(RMotorFPin, LOW);
    digitalWrite(RMotorRPin, LOW);
}

void MotorControl(){
    /*
    Sending PWM-signals to the motor-controllers
    */
    int RMotorValue = 0;
    int LMotorValue = 0;
    //reading the data from array which is being provided through the serial-connection
    RMotorValue = readJsonValue("RightMotor");
    LMotorValue = readJsonValue("LeftMotor");
    //Motor turns clockwise if value is greater 0 else turns counterclockwise. Those are different pins though.
    // Todo: the lines 94-116 can be moved to a separate function to make it more modular!
    if (RMotorValue < 0){
        analogWrite(RMotorRPin, abs(RMotorValue));
//        Serial.println(RMotorValue);  // debugging-line
    }
    else if(RMotorValue > 0){
        analogWrite(RMotorFPin, RMotorValue);
//        Serial.println(RMotorValue);  // debugging-line
    }
    else{
        SetRightMotorsZero();
    }
    //data[3] is bool and decides if LMotor is turning clockwise or counterclockwise
    if (LMotorValue < 0){
        analogWrite(LMotorRPin, abs(LMotorValue));
//        Serial.println(LMotorValue);  // debugging-line
    }
    else if (LMotorValue > 0){
        analogWrite(LMotorFPin, LMotorValue);
//        Serial.println(LMotorValue);  // debugging-line
    }
    else {
        SetLeftMotorsZero();
    }
}

void ServoControl() {
    /*
    Moving servos with the help of a library which talks to the servos through PWM
    */
    //Setting the values from Json-document which is being provided through the serial-connection
    int CameraXValue = readJsonValue("CameraXServo");
    long int RStickXValue;
    //fitting the values from -255 - 255 to 0-180°
    RStickXValue = map(RStickXValue, -254, 254, 0, 180);
    //Turning the servos
    XServo.write(RStickXValue);
}
