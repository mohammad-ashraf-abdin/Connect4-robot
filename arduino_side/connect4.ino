#include <Servo.h>

Servo myservo;

int RPWM_Output = 5; // Arduino PWM output pin 5; connect to IBT-2 pin 1 (RPWM)
int LPWM_Output = 6; // Arduino PWM output pin 6; connect to IBT-2 pin 2 (LPWM)
int encoderPin1 = 2;
int encoderPin2 = 3;

int motorButton = 4;
int playerButton = 8 ;

volatile int lastEncoded = 0;
volatile long encoderValue = 0;

long lastencoderValue = 0;

int temp = 0 ;

bool pressed = 0;

int lastMSB = 0;
int lastLSB = 0;
int errorValue = 50;
void setup() {
  Serial.begin(9600);
  myservo.attach(9);
  pinMode(RPWM_Output, OUTPUT);
  pinMode(LPWM_Output, OUTPUT);
  pinMode(motorButton, INPUT);
  pinMode(playerButton, INPUT);
  pinMode(encoderPin1, INPUT);
  pinMode(encoderPin2, INPUT);

  digitalWrite(encoderPin1, HIGH); //turn pullup resistor on
  digitalWrite(encoderPin2, HIGH); //turn pullup resistor on

  //call updateEncoder() when any high/low changed seen
  //on interrupt 0 (pin 2), or interrupt 1 (pin 3)
  attachInterrupt(0, updateEncoder, CHANGE);
  attachInterrupt(1, updateEncoder, CHANGE);
  encoderRest();
}

void loop()
{
  //  analogWrite(LPWM_Output,50);
  //  analogWrite(RPWM_Output, 0);
  //  Serial.println(encoderValue);
  // reverse rotation

  // analogWrite(LPWM_Output,125);
  // analogWrite(RPWM_Output, 0);
  //  Serial.println(digitalRead(4));
  // motorMove(-2000);

  //  Serial.println(encoderValue);
  //  for (int i = 0 ; i < 6400; i + 100)
  //  {
  //    analogWrite(LPWM_Output, 50);
  //    analogWrite(RPWM_Output, 0);
  //    Serial.println(encoderValue);
  //    while (!digitalRead(4))
  //    { analogWrite(LPWM_Output, 0);
  //      analogWrite(RPWM_Output, 0);
  //      Serial.print("");
  //    }
  //  }
  //
  if (digitalRead(playerButton) && !pressed)
  {
    pressed = true;
    Serial.print("1");
    delay(500);
  }
  else if (!digitalRead(playerButton)) {
    pressed = false;

  }
  if (Serial.available())
  {
    char readed = Serial.read();
    switch (readed)
    {
      case ('1'):
        {
          motorMove(-1800);
          break;
        }
      case ('2'):
        {
          motorMove(-2480);
          break;
        }
      case ('3'):
        {
          motorMove(-3375);
          break;
        }
      case ('4'):
        {
          motorMove(-4150);
          break;
        }
      case ('5'):
        {
          motorMove(-5100);
          break;
        }
      case ('6'):
        {
          motorMove(-5800);
          break;
        }
      case ('7'):
        {
          motorMove(-6730);
          break;
        }
      case ('p'):
        {
          stackPop();
          break;
        }
      case ('r'):
        {
          encoderRest();
          break;
        }
      default:
        break;
    }
    delay(1000);
    encoderRest();
  }


}
void stackPop()
{
  myservo.write(140);
  delay (2000);
  myservo.write(0);

}
void encoderRest()
{
  while (!digitalRead(motorButton))
  {
    analogWrite(LPWM_Output, 0);
    analogWrite(RPWM_Output, 50);
  }
  analogWrite(LPWM_Output, 0);
  analogWrite(RPWM_Output, 0);
  lastEncoded = 0;
  encoderValue = 0;
  lastencoderValue = 0;
  lastMSB = 0;
  lastLSB = 0;
}
void motorMove (int x )
{
  if (encoderValue  > x || encoderValue  > x + errorValue || encoderValue  > x - errorValue )
  {
    while (encoderValue > x)
    {
      analogWrite(LPWM_Output, 50);
      analogWrite(RPWM_Output, 0);
    }
    analogWrite(LPWM_Output, 0);
    analogWrite(RPWM_Output, 0);
    stackPop();
  }
  else if (encoderValue  < x || encoderValue  < x + errorValue || encoderValue  < x - errorValue) {
    while (encoderValue < x)
    {
      analogWrite(LPWM_Output, 0);
      analogWrite(RPWM_Output, 50);
    }
    analogWrite(LPWM_Output, 0);
    analogWrite(RPWM_Output, 0);
    stackPop();

  }
  else {
    analogWrite(LPWM_Output, 0);
    analogWrite(RPWM_Output, 0);
  }
}


void updateEncoder() {
  int MSB = digitalRead(encoderPin1); //MSB = most significant bit
  int LSB = digitalRead(encoderPin2); //LSB = least significant bit

  int encoded = (MSB << 1) | LSB; //converting the 2 pin value to single number
  int sum = (lastEncoded << 2) | encoded; //adding it to the previous encoded value
  if (sum == 0b1101 || sum == 0b0100 || sum == 0b0010 || sum == 0b1011)
    encoderValue ++;
  if (sum == 0b1110 || sum == 0b0111 || sum == 0b0001 || sum == 0b1000)
    encoderValue --;
  lastEncoded = encoded; //store this value for next time
}
