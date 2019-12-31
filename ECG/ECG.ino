/******************************************************************************
Electrocardiograma AD8232
******************************************************************************/

void setup() {
  // Iniciar comunicación serial
  Serial.begin(9600);
}

void loop() {
  
 Serial.println(analogRead(A0));
 delay(1);
}
