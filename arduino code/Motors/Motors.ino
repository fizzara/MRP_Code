const int topL = 3;
const int topR = 4;
const int botL = 5;
const int botR = 6;
const int mid = 7;
int incomingByte = 0;

void setup() {
  pinMode(topL, OUTPUT);
  pinMode(topR, OUTPUT);
  pinMode(botL, OUTPUT);
  pinMode(botR, OUTPUT);
  pinMode(mid, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  Serial.println(incomingByte);
  // send data only when you receive data:
  if(incomingByte == 48){
    analogWrite(topL, 0);
    analogWrite(topR, 0);
    analogWrite(botL, 0);
    analogWrite(botR, 0);
    analogWrite(mid, 0);
  }
  if (Serial.available() > 0) {
    // read the incoming byte:
    incomingByte = Serial.read();

    // say what you got:
    Serial.print("I received: ");
    Serial.println(incomingByte);
    if(incomingByte == 48){
      analogWrite(topL, 0);
      analogWrite(topR, 0);
      analogWrite(botL, 0);
      analogWrite(botR, 0);
      analogWrite(mid, 0);
    }
    if(incomingByte == 49){
      enemyTL();
      incomingByte = 48;
    }
    if(incomingByte == 50){
      enemyTR();
      incomingByte = 48;
    }
    if(incomingByte == 51){
      enemyBL();
      incomingByte = 48;
    }
    if(incomingByte == 52){
      enemyBR();
      incomingByte = 48;
    }
    if(incomingByte == 53){
      enemyM();
      incomingByte = 48;
    }
  }
}


void enemyTL(){
  analogWrite(topL, 255);
  delay(1000);
  analogWrite(topL, 0);
}

void enemyTR(){
  analogWrite(topR, 255);
  delay(1000);
  analogWrite(topR, 0);
}

void enemyBL(){
  analogWrite(botR, 255);
  delay(1000);
  analogWrite(botR, 0);
}

void enemyBR(){
  analogWrite(botL, 255);
  delay(1000);
  analogWrite(botL, 0);
}

void enemyM(){
  analogWrite(mid, 255);
  delay(1000);
  analogWrite(mid, 0);
}  