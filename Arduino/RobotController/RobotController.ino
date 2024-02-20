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
    static byte serialByteData[maxMessageSize];
    SetMotorsZero();
    ReadSerialConnection(serialByteData);
    //Sending transformed data to motors and servos
    MotorControl(serialByteData);
    //ServoControl(serialByteData);
    //Serial.println(String(serialByteData[0]) + ' ' + String(serialByteData[2]));
    delay(50);
}

void ReadSerialConnection(byte* serialByteData){
    char serialData[5]; // assuming max 4 digits number and 1 place for null character
    byte serialDataIndex = 0;

    while(Serial.available()){
        char incomingByte = Serial.read();

        // Check if incoming byte is separator or end of message.
        if(incomingByte == ',' || incomingByte == '&'){
            // Null-terminate the temporary character array and convert it to integer.
            serialData[serialDataIndex] = '\0';
            serialByteData[serialDataIndex] = atoi(serialData);

            // Clean up for the next integer.
            memset(serialData, 0, sizeof(serialData));
            serialDataIndex = 0;
        }else{
            // Add incoming byte to our temporary array.
            serialData[serialDataIndex++] = incomingByte;
        }

        // Break if you've reached the end of the message.
        if(incomingByte == '&'){
            break;
        }
    }
}

void SetMotorsZero(void){
    //Setting the motor-pins low in each iteration. If something gets stuck or communication breaks robot will stop!
    digitalWrite(LMotorFPin, LOW);
    digitalWrite(LMotorRPin, LOW);
    digitalWrite(RMotorFPin, LOW);
    digitalWrite(RMotorRPin, LOW);
}

void MotorControl(byte serialByteData[maxMessageSize]){
    /*
    Sending PWM-signals to the motor-controllers
    */
    byte RMotorValue = 0;
    byte LMotorValue = 0;
    //reading the data from array which is being provided through the serial-connection
    RMotorValue = serialByteData[0];
    LMotorValue = serialByteData[2];
//    Serial.println("RMotor: "+ String(RMotorValue) + " LMotor: " + String(LMotorValue));  // debugging-line
//    Serial.println("ARRAYDATA: " + arrayData[0] + arrayData[1] + arrayData[2] + arrayData[3]);  // debugging-line
    //data[1] is bool and decides if RMotor is turning clockwise or counterclockwise
    if (serialByteData[1] == 1){
        analogWrite(RMotorRPin, RMotorValue);
//        Serial.println(RMotorValue);  // debugging-line
    }
    else{
        analogWrite(RMotorFPin, RMotorValue);
//        Serial.println(RMotorValue);  // debugging-line
    }
    //data[3] is bool and decides if LMotor is turning clockwise or counterclockwise
    if (serialByteData[3] == 1){
        analogWrite(LMotorRPin, LMotorValue);
//        Serial.println(LMotorValue);  // debugging-line
    }
    else{
        analogWrite(LMotorFPin, LMotorValue);
//        Serial.println(LMotorValue);  // debugging-line
    }
}

void ServoControl(byte serialByteData[maxMessageSize]) {
    /*
    Moving servos with the help of a library which talks to the servos through PWM
    */
    //Setting the values from array which is being provided through the serial-connection
    byte RStickXValuePos = serialByteData[4];
    byte RStickXValueNeg = serialByteData[5];
    byte RStickYValuePos = serialByteData[6];
    byte RStickYValueNeg = serialByteData[7];
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
