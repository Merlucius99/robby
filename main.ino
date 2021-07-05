//Include the Wire library for I2C
#include <Wire.h>
#include <SharpIR.h>
#include <DHT.h>
#include <RF24.h> 

#define DHTTYPE DHT11   // DHT 11
#define ir A0
#define model 20150
SharpIR SharpIR(ir, model);


RF24 radio(9, 10) ;  // ce, csn pins    
const byte addresses [][6] = {"00001", "00002"};  //Setting the two addresses. One for transmitting and one for receiving

const int pwm_servo = 3;
const int BATTERY_PIN = A6;
const int DHTPIN = 2;
int LEFT_PIN = A1;
int MIDDLE_PIN = A2;
int RIGHT_PIN = A3;

int temp;
int humidity;
int fire;
int payload[17];
boolean statusPayload;
int joystick[3];
int index = 0;
boolean resetPayload = true;

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600) ;
  pinMode(pwm_servo, OUTPUT);
  
  // Join I2C bus as slave with address 8
  Wire.begin(0x8);
  payload[18]=23;

  dht.begin();
  delay(1000);
  updateValues();
  radioSetup();
  
  // Call receiveEvent when data received
  Wire.onReceive(receiveEvent);
  Wire.onRequest(sendEvent);
  Serial.println("READY...");
}

void updateValues(){
  Serial.println();
  delay(100);
  temp = dht.readTemperature();
  if(temp >= 50 || temp <= 0)
  {
    temp = 0; 
  }
  Serial.print("temp = ");
  Serial.println(temp);
  delay(100);
  payload[0] = temp;
  
  humidity = dht.readHumidity();
  if(humidity >= 80 || humidity <= 20)
  {
    humidity = 0; 
  }
  Serial.print("humidity = ");
  Serial.println(humidity);
  delay(100);
  payload[1] = humidity;
  
  checkFire();
  delay(100);
  payload[2] = fire;
  
  scanRoom();
  
  resetPayload = false;
  statusPayload = true;
  
  }

void radioSetup(){
  if(radio.begin())   // start radio at ce csn pin 9 and 10
  {
      Serial.println("Radio OK");
  }
  radio.openWritingPipe(addresses[1]);     //Setting the address at which we will send the data
  radio.openReadingPipe(1, addresses[0]);  //Setting the address at which we will receive the data
  radio.setPALevel(RF24_PA_MIN); //You can set it as minimum or maximum depending on the distance between the transmitter and receiver. 
}
  
float getBatteryVoltage(){
    float v[40];
    int count[40];
    int max[] = {0,0,0};
    for(int i=0; i<40; i++){
        float val = analogRead(BATTERY_PIN);
        float vlotage = (val*5)/1024;
        v[i] = vlotage;
        for(int j=0; j<i; j++){
            if(v[j] == val){
                count[i]++;
                if(max[1] > count[i]){
                    max[0] = i;
                    max[1] = count[i];
                  }
              }
          }
      }
    return (v[max[0]]);
  }
  
void checkFire(){
  int LEFT_PIN_VALUE = analogRead(LEFT_PIN);
  int MIDDLE_PIN_VALUE = analogRead(MIDDLE_PIN);
  int RIGHT_PIN_VALUE = analogRead(RIGHT_PIN);
  
  int TRIGGER = 400;
  fire =0;
    if(LEFT_PIN_VALUE >= TRIGGER){
      fire += 100;
    }
    if(MIDDLE_PIN_VALUE >= TRIGGER){
      fire += 10;
    }
    if(RIGHT_PIN_VALUE >= TRIGGER){
      fire += 1;
    }
  }

int getDistance(){
unsigned long pepe1=millis();
    while(true){
        int v1 = SharpIR.distance();
        delay(50);
        int v2 = SharpIR.distance();
        delay(50);
        int v3 = SharpIR.distance();
        delay(50);
        unsigned long pepe2=millis()-pepe1;
        if(pepe2 >= 1000){
          delay(1);
          return 101;
        }
        if(v1 >= 85 || v2 >= 85 || v3 >= 85){
          delay(1);
          return 100;
        }
        if(abs(v1-v2) <= 5 && abs(v3-v2) <= 5){
          delay(1);
          if(v2 == 0) return 100;
          return v2;       
        }
        
      }
    
  }

int measureAtPosition(int pos){
    analogWrite(pwm_servo, pos);
    delay(100);
    return getDistance();
  }

void scanRoom(){
    for(int i=44; i<255; i=i+21){
        int j = (i-44)/21+3;
        payload[j] = measureAtPosition(i);
      }
    analogWrite(pwm_servo, 44);
    delay(100);
  }

// Function that executes whenever data is received from master
void receiveEvent(int payload){

     while (Wire.available()){ // loop through all but the last
        Serial.print("Receving: ");
        int c = Wire.read(); // receive byte as a character
        String text = String(c);
        Serial.println(text);
        int index = text.toInt();
      }

  }

void sendEvent() {
    Wire.write(payload[index]);       // sends one byte
//    Serial.print(index);
//    Serial.print("-"); 
//    Serial.print(payload[index]);
//    Serial.print(" "); 
    index++;
    if(index >= 17){
      index = 0;
      resetPayload = true;    
      }
  }
  
void print_array(int size, int v[])
{
  Serial.print("DATA = ");
  for(int i = 0 ;i < size; i++)
  {
    Serial.print(v[i]);
    Serial.print(" ");
  }
  Serial.println();
}

void radioRecieved(){
  radio.startListening() ;        // start listening - added acum
  unsigned long pepe1=millis();
  char receivedMessage[3];   // set incmng message for 32 bytes
  while(!radio.available()){
      unsigned long pepe2=millis()-pepe1;
      if(pepe2 >= 100)
        return;
    }
  radio.read(&joystick[0],sizeof(joystick));    // read the message and save
  payload[14] = joystick[0]/5;
  payload[15] = joystick[1]/5;
  payload[16] = joystick[2];
  print_array(3, joystick);
}

void radioSend(){
    delay(5);
    radio.stopListening();
    radio.write(&payload[0], sizeof(payload[0])*3);
    radio.write(&x[0], sizeof(x[0])*11);
    radio.write(&y[0], sizeof(y[0])*11);
    print_array(17, payload);  
    delay(5);    
}

void loop() {
  if(resetPayload == true){
    updateValues();
    //print_array(17,payload);
    }
  radioSend();
  radioRecieved();
  delay(500);
}
