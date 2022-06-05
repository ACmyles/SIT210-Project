int soilSensor = 0;
int soilSensor2 = 0;

void setup() {
    Serial.begin(9600);
    Particle.variable("soilSensor", &soilSensor, INT);
    Particle.variable("soilSensor2", &soilSensor2, INT);
    pinMode(A0, INPUT);
    pinMode(A1, INPUT);
}
void loop() {
    soilSensor = analogRead(A0);
    soilSensor2 = analogRead(A1);
    delay(1000);
}