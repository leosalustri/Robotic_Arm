//Ottenere i pass encoder gestendo due motori per arduino.

//Motore a
#define encoderA 2
#define d_encoderA 4
volatile long EncoderCounterA = 0; 

//Motore b
#define encoderB 3
#define d_encoderB 8
volatile long EncoderCounterB = 0; 

//Time 
#define sampling_time 50 //microseconds
unsigned long oldtime = 0;

//Altre costanti
#define alfa 0.6 //valore di alfa appartenente a [0,1]
#define Kp = 1000;
#define Kd = 1000;

void setup(){
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
  if(micros()-oldtime > sampling_time){
    oldtime = micros();  
    EncoderCounterA = constrain(EncoderCounterA,-1E6,1E6);
    EncoderCounterB = constrain(EncoderCounterB,-1E6,1E6);
    Serial.print(EncoderCounterA,DEC);
    Serial.print(",  ");
    Serial.println(EncoderCounterB,DEC);
        

    
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

//Funzione di filtraggio dell'uscita di alimentazione del motore in PWM
float filter(float u)
{
  float uf;
  uf = u*alfa +(1-alfa)*u;
  return uf;
}




