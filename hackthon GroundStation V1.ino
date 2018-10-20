const int temp = A0;      //DEFINE SENSOR LM35 LIGADO AO PINO ANALOGICO A0
const int nivel = A1;     //DEFINE PINO NÍVEL TANQUE LIGADO AO PINO ANALOGICO A1
const int turbi = A2;     //DEFINE PINO SENSOR TURBIDEZ LIGADO AO PINO ANALOGICO A2
const int D8 = 8;
const int D13 = 13;

float temperatura; 
int nivel1;
float turbidez;
float m;
float temperatura1;
 
void setup() {
Serial.begin(9600);
}

 
void loop() {
temperatura = (analogRead(temp));
float m = (temperatura/1024.0)*5000;
float temperatura1 = m/10;
nivel1 = (int(analogRead(nivel)));
turbidez = (analogRead(turbi))* (5.0 / 1024.0);
pinMode(D8, OUTPUT);
pinMode(D13, OUTPUT);


Serial.print("T");
Serial.println(temperatura1);
Serial.print("N");
Serial.println(nivel1);
Serial.print("Z");
Serial.println(turbidez);

if (nivel1>90){
    digitalWrite(D8, LOW);
    digitalWrite(D13, LOW);
}else{
    digitalWrite(D8, HIGH);
    digitalWrite(D13, HIGH);
}
delay(1000);
}
