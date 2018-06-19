#include <Servo.h>

//Set up the servo motors
Servo Motor1, Motor2, Motor3, Water;

void setup() {
  Serial.begin(9600); //set up serial monitor to be used for reading in
  Motor1.attach(9);   // Setup a servo for pills in pin 9
  Motor2.attach(10);   // Setup a servo for pills in pin 10
  Motor3.attach(11);   // Setup a servo for pills in pin 11
  Water.attach(8);     // Setup a servo for the water in pin 8
  // Make sure everything is off and closed
  Motor1.write(90);
  Motor2.write(90);
  Motor3.write(90);
  Water.write(0);
}

void loop() {
  // Will be used to determine if any pills have been dispensed
  bool water = false;

  int num(0), num1(0), num2(0), one(0), two(0), three(0), n(0), n1(0), n2(0);

  // Initialize the input to ""
  String value = "";

  // Make sure everything is stopped
  Motor1.write(90);
  Motor2.write(90);
  Motor3.write(90);

  // Because of how fast the serial data gets sent from the python file it is all read as one string
  if (Serial.available()) {         // If the serial monitor is open then read it
    value = Serial.readString();    // Read in the string from the serial

    // Now we have to do some computation to determine what motors to turn on and for how long
    // We are assisted in the fact that a motor will not be told to turn on before a motor after it
    // i.e. Motor 3 will not be told to turn on before Motor 1, therefore if Motor 1 needs to be on it will always be
    //      in the first position
    // There will be three cases: one motor told to be on, two motors told to be on, or all three motors told to be on

    // n corresponds to which motor to turn on
    // num corresponds to the number of pills being sent
    if (value.length() == 2) {
      n = value.toInt() / 10;
      num = value.toInt() % 10;
    }
    else if (value.length() == 4) {
      one = value.substring(0, 2).toInt();
      n = one / 10;
      num = one % 10;
      two = value.substring(2).toInt();
      n1 = two / 10;
      num1 = two % 10;
    }
    else if (value.length() == 6) {
      one = value.substring(0, 2).toInt();
      n = one / 10;
      num = one % 10;
      two = value.substring(2, 4).toInt();
      n1 = two / 10;
      num1 = two % 10;
      three = value.substring(4).toInt();
      n2 = three / 10;
      num2 = three % 10;
    }
  }

  // All of the if statements behave similarly to the following

  if (n == 1) {             // Will read a one from the parent python program
    Motor1.write(0);        // Turn the motor on
    delay(1300 * num);      // Wait one rotation for each pill
    Motor1.write(90);       // Turn the motor off
    n = 0;                  // Set n back to 0 so it doesn't enter again
    num = 0;                // Set the number of pills back to 0
    water = true;           // Allow the water to turn on since a pill has been dispensed
  }
  if (n == 2) {
    Motor2.write(0);
    delay(1300 * num);
    Motor2.write(90);
    n = 0;
    num = 0;
    water = true;
  }
  else if (n1 == 2) {
    Motor2.write(0);
    delay(1300 * num1);
    Motor2.write(90);
    n1 = 0;
    num1 = 0;
    water = true;
  }
  if (n == 3) {
    Motor3.write(0);
    delay(1300 * num);
    Motor3.write(90);
    n = 0;
    num = 0;
    water = true;
  }
  else if (n1 == 3) {
    Motor3.write(0);
    delay(1300 * num1);
    Motor3.write(90);
    n1 = 0;
    num1 = 0;
    water = true;
  }
  else if (n2 == 3) {
    Motor3.write(0);
    delay(1300 * num2);
    Motor3.write(90);
    n2 = 0;
    num2 = 0;
    water = true;
  }
  if (water) {
    Water.write(90);
    delay(6000);            // A decent amount of water took about six seconds of dispensing
    Water.write(0);
    water = false;
  }
}
