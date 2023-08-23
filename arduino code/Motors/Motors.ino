const int tL = 3;
const int tR = 4;
const int bR = 5;
const int bL = 6;

void setup() {
  pinMode(tL, OUTPUT);
  pinMode(tR, OUTPUT);
  pinMode(bR, OUTPUT);
  pinMode(bL, OUTPUT);

}

void loop() {

  analogWrite(tL, 127);
  delay(1000);
  analogWrite(tL, 255);
  
  delay(1000);
}

void topLeft(){
  analogWrite(tL, 255)
}