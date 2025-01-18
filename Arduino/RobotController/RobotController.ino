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
    ServoControl();
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
    _evaluateMotorDirection(RMotorFPin, RMotorRPin, RMotorValue);
    _evaluateMotorDirection(LMotorFPin, LMotorRPin, LMotorValue);
}

void _evaluateMotorDirection(unsigned short forwardMotorPin,unsigned short rewardMotorPin, int motorValue){
    /*
    Method for turning a motor forward or backward.
    :param motorPin: the pin of the motor that will be controlled.
    :param motorValue: the value of the motor, deciding the speed and direction of the motor (<0 backward, >0 forward)
    */
    if (motorValue < 0){
        analogWrite(rewardMotorPin, abs(motorValue));
//        Serial.println(LMotorValue);  // debugging-line
    }
    else if (motorValue > 0){
        analogWrite(forwardMotorPin, motorValue);
//        Serial.println(LMotorValue);  // debugging-line
    }
    else {
        SetMotorsZero();
    }
}

void ServoControl() {
    /*
    Moving servos with the help of a library which talks to the servos through PWM
    */
    //Setting the values from Json-document which is being provided through the serial-connection
    int CameraXValue = readJsonValue("CameraXServo");
    int CameraZValue = readJsonValue("CameraZServo");
    _evaluateServoDirection(XServo, CameraXValue);
    _evaluateServoDirection(ZServo, CameraZValue);
}

void _evaluateServoDirection(Servo servo, int servoValue){
    /*
    Method for turning a servo by an angle, that is being represented through an integer (-32768 to 32767).
    :param servo: Servo that will be controlled.
    :param servoValue: Value which will be translated into an angle.
    */
    int valueMappedToDegree = map(servoValue, -32768, 32767, 0, 180);
    servo.write(valueMappedToDegree);
}