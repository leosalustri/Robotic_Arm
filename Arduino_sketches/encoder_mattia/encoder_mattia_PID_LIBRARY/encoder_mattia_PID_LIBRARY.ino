#include <PID_v1.h>
//Ottenere i pass encoder gestendo due motori per arduino.

//PID params and variables
double Setpoint;
double Input;
double Output;
double Kp = 8 , Ki =100 , Kd=0.01;
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

//Time 
#define sampling_time 50 //microseconds
unsigned long oldtime = 0;


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
  oldtime = micros();
}

void loop()
{
  //delta t = 50 millisec
  if(micros()-oldtime > sampling_time){
    oldtime = micros();  
    EncoderCounterA = constrain(EncoderCounterA,-1E6,1E6);
    EncoderCounterB = constrain(EncoderCounterB,-1E6,1E6);
    Serial.print(EncoderCounterA,DEC);
    Serial.print(",  ");
    Serial.println(EncoderCounterB,DEC);

    
    Setpoint = -1050;//Voglio che il motore faccia 90°
    Input = EncoderCounterA;
    if(Setpoint >0)
      {
            //Senso Antiorario
            digitalWrite(left,HIGH);
            digitalWrite(right,LOW);
            mypid.SetControllerDirection(DIRECT);
      }else{
          digitalWrite(left, LOW);
          digitalWrite(right, HIGH);
          mypid.SetControllerDirection(REVERSE);
      }
    
    mypid.Compute();
    analogWrite(pwm, Output);
    
       
  }  
    
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
