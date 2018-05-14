#include <PID_v1.h>

//Ottenere i pass encoder gestendo due motori per arduino.

//PID params and variables
double Setpoint;
double Input;
double Output;
double Kp = 4500 , Ki = 200, Kd=1000;
PID mypid(&Input, &Output,&Setpoint, Kp, Ki, Kd, DIRECT);

//Motore a
#define encoderA 2
#define d_encoderA 4
volatile long EncoderCounterA = 0; 
#define pwm 11
#define left 12
#define right 13


//Motore b
#define encoderB 3
#define d_encoderB 8
volatile long EncoderCounterB = 0; 



int pos;
void moveMotor(int passi);

void setup(){
  mypid.SetMode(AUTOMATIC);
  mypid.SetTunings(Kp, Ki, Kd);
  
  pinMode(pwm, OUTPUT);
  pinMode(right, OUTPUT);
  pinMode(left, OUTPUT);
    
  pinMode(encoderA, INPUT); 
  digitalWrite(encoderA, HIGH); 
  pinMode(d_encoderA, INPUT); 
  digitalWrite(d_encoderA, HIGH);  
  pinMode(encoderB, INPUT); 
  digitalWrite(encoderB, HIGH);  
  pinMode(d_encoderB, INPUT); 
  digitalWrite(d_encoderB, HIGH);  
  
  //Interrupt Routine
  attachInterrupt(0, doEncoderA, CHANGE);
  attachInterrupt(1, doEncoderB, CHANGE);
  Serial.begin(9600);
  //pos = 1050;
}

void loop()
{
    EncoderCounterA = constrain(EncoderCounterA,-1E6,1E6);
    EncoderCounterB = constrain(EncoderCounterB,-1E6,1E6);
    Serial.print(EncoderCounterA,DEC);
    Serial.print(",  ");
    //Serial.print(Output, DEC);
    //Serial.print(",  ");
    //Serial.println(pos, DEC);
    //Serial.print(",  ");
    //Serial.println(EncoderCounterB,DEC);
    if(Serial.available()>0){
      pos = Serial.parseInt();
      
    }
    else {
      pos = pos;
    }

    Serial.println(pos, DEC);
    moveMotor(pos);  
   
}


//Edited interrupt service routine
void doEncoderA(){ 
  if(digitalRead(d_encoderA)){
          if(digitalRead(encoderA))
                  EncoderCounterA++;}
         else {
                if(digitalRead(encoderA)) EncoderCounterA--;
                }
         }

//Original interrupt service routine
void doEncoderB(){ 
  if(digitalRead(d_encoderB)){
          if(digitalRead(encoderB))
                  EncoderCounterB++;}
         else {
                if(digitalRead(encoderB)) EncoderCounterB--;
                }
   }

void moveMotor(int passi){
  
//Controlla la direzione :Negativo senso orario
if(passi >EncoderCounterA)
      {
            //Senso Antiorario
            digitalWrite(left,LOW);
            digitalWrite(right,HIGH);
            mypid.SetControllerDirection(DIRECT);
      }else{
          digitalWrite(left, HIGH);
          digitalWrite(right, LOW);
          mypid.SetControllerDirection(REVERSE);
      }
    //fa fermare il motore se ha raggiunto tale valore di encoder ,evita inoltre il tremolio  
  if(EncoderCounterA>passi -10 and EncoderCounterA < passi + 10)
    {
      analogWrite(pwm, 0); 
    }
  else {
  Input = EncoderCounterA;
  Setpoint = passi;
  mypid.Compute();
  analogWrite(pwm, Output);
 }
  
}

