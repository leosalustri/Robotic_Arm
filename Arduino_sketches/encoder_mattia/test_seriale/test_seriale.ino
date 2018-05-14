#define vcc 8
#define gnd 4
int value = 0;

void setup() {
  Serial.begin(9600);
  pinMode(vcc,OUTPUT);
  pinMode(gnd, OUTPUT);
}

void loop() {
  if(Serial.available()>0){
    value = Serial.parseInt();
    digitalWrite(vcc, HIGH);
    digitalWrite(gnd, LOW);
    Serial.println(value, DEC);
  }
}
