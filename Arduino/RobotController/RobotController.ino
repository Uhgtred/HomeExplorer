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
StaticJsonDocument<80> jsonDocument;

const unsigned short maxMessageSize = 80;

Servo XServo;
Servo ZServo;

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
    //ZServo.write(90);
}

void loop() {
    //Setting the motor-pins low in each iteration. If something gets stuck or communication breaks robot will stop!
    SetMotorsZero();
    String jsonData = readSerialJson();
    //Sending transformed data to motors and servos
    MotorControl();
    //ServoControl();
    //Serial.println(String(serialByteData[0]) + ' ' + String(serialByteData[2]));
    delay(50);
}

int readJsonValue(String key){
    int value = jsonDocument[key];
    return value;
}

void readSerialJson(){
    if (Serial.available()){
        String jsonData = Serial.readStringUntil('&');
        // storing json into global json document
        deserializeJson(jsonDocument, jsonData);
    }
}



//void ReadSerialConnection(byte* serialByteData){
//    char serialData[5]; // assuming max 4 digits number and 1 place for null character
//    byte serialDataIndex = 0;
//
//    while(Serial.available()){
//        char incomingByte = Serial.read();
//
//        // Check if incoming byte is separator or end of message.
//        if(incomingByte == ',' || incomingByte == '&'){
//            // Null-terminate the temporary character array and convert it to integer.
//            serialData[serialDataIndex] = '\0';
//            serialByteData[serialDataIndex] = atoi(serialData);
//
//            // Clean up for the next integer.
//            memset(serialData, 0, sizeof(serialData));
//            serialDataIndex = 0;
//        }else{
//            // Add incoming byte to our temporary array.
//            serialData[serialDataIndex++] = incomingByte;
//        }
//
//        // Break if you've reached the end of the message.
//        if(incomingByte == '&'){
//            break;
//        }
//    }
//}

void SetMotorsZero(void){
    //Setting the motor-pins low in each iteration. If something gets stuck or communication breaks robot will stop!
    digitalWrite(LMotorFPin, LOW);
    digitalWrite(LMotorRPin, LOW);
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
    RMotorValue = readJsonValue("5");
    LMotorValue = readJsonValue("2");
//    Serial.println("RMotor: "+ String(RMotorValue) + " LMotor: " + String(LMotorValue));  // debugging-line
//    Serial.println("ARRAYDATA: " + arrayData[0] + arrayData[1] + arrayData[2] + arrayData[3]);  // debugging-line
    //data[1] is bool and decides if RMotor is turning clockwise or counterclockwise
    if (RMotorValue < 0){
        analogWrite(RMotorRPin, RMotorValue);
//        Serial.println(RMotorValue);  // debugging-line
    }
    else{
        analogWrite(RMotorFPin, RMotorValue);
//        Serial.println(RMotorValue);  // debugging-line
    }
    //data[3] is bool and decides if LMotor is turning clockwise or counterclockwise
    if (LMotorValue < 0){
        analogWrite(LMotorRPin, LMotorValue);
//        Serial.println(LMotorValue);  // debugging-line
    }
    else{
        analogWrite(LMotorFPin, LMotorValue);
//        Serial.println(LMotorValue);  // debugging-line
    }
}

void ServoControl() {
    /*
    Moving servos with the help of a library which talks to the servos through PWM
    */
    //Setting the values from array which is being provided through the serial-connection
    int RStickXValue = readJsonValue("3");
    //XServo.writeMicroseconds(1500);
    //fitting the values from 0-255 to 0-180°
    RStickXValue = map(RStickXValue, -254, 254, 0, 180);
    //Turning the servos
    XServo.write(RStickXValue);
}
