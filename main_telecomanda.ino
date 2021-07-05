#include <Wire.h> 
#include <LiquidCrystal_I2C.h>
#include <RF24.h> 
#include <SPI.h>
#include "Ucglib.h"

#define ARRAY_SIZE(array) ((sizeof(array))/(sizeof(array[0])))
Ucglib_ST7735_18x128x160_SWSPI ucg(/*sclk=*/ 13, /*data=*/ 11, /*cd=*/ 9 , /*cs=*/ 10, /*reset=*/ 8);
RF24 radio(9, 10) ;  // ce, csn pins    
const byte addresses [][6] = {"00001", "00002"};
int line = 1;
int count=0;
char temp[32];
LiquidCrystal_I2C lcd(0x27,16,2);

boolean statusPayload;
int payload[3];
int x[11];
int y[11];
int joystick[3];
String joystickValue;
String payloadValue;


void setup() {
  while (!Serial) ;
  Serial.begin(9600) ;     // start serial monitor baud rate
  Serial.println("Starting.. Setting Up.. Radio on..") ; // debug message
    
  Wire.begin();
  delay(1000);
  ucg.begin(UCG_FONT_MODE_SOLID);
  ucg.clearScreen();
  ucg.setColor(0, 0, 0);
  ucg.setRotate180();

  //radioSetup();
  lcd.init();
  lcd.backlight();

  lcd.setCursor(0,0);
  lcd.print("Hello, Andrei! ");
  delay(1000);

  //setupTFT();
  
  pinMode(2, INPUT_PULLUP);  
}
void setupTFT(){
  ucg.begin(UCG_FONT_MODE_SOLID);
  ucg.clearScreen();
  ucg.setColor(0, 0, 0);
  ucg.setRotate180();

  }

void radioSetup(){
  if(radio.begin())   // start radio at ce csn pin 9 and 10
  {
      Serial.println("Radio OK");
  }
  radio.openWritingPipe(addresses[0]);     //Setting the address at which we will send the data
  radio.openReadingPipe(1, addresses[1]);  //Setting the address at which we will receive the data
  radio.setPALevel(RF24_PA_MIN); //You can set it as minimum or maximum depending on the distance between the transmitter and receiver. 
}

void radioTrans(){
  delay(5);
  radio.startListening();                    //This sets the module as receiver
  if (radio.available())                     //Looking for incoming data
  {
  radio.read(&payload[0], sizeof(payload[0])*3);
  radio.read(&x[0], sizeof(x[0])*11);
  radio.read(&y[0], sizeof(y[0])*11);
  print_array(3, payload);
  print_array(11, x);
  print_array(11, y);
  payloadValue = "T:" + String(payload[0]) + " H:" + String(payload[1]) + " F:" + String(payload[2]);
  delay(5);
  radio.stopListening();
  radio.write(&joystick[0], sizeof(joystick)); 
  }
  }

void readJoystick(){
  joystick[0] = analogRead(A1);
  joystick[1] = analogRead(A0);
  joystick[2] = digitalRead(2);
  String x=String(joystick[0]);
  String y=String(joystick[1]);
  String sw=String(joystick[2]);
  joystickValue = x+"-"+y+"-"+sw;
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

void plotRoom(int x[], int y[], int elementCount){
  ucg.clearScreen();
  ucg.setColor(0, 0, 0);
  float maxX=0;
  float maxY=0;
  for(int i=0; i<elementCount; i++){
    if(abs(x[i])>maxX)
      maxX = abs(x[i]);
    if(abs(y[i])>maxY)
      maxY = abs(y[i]);
    }
  float offsetX = 128/maxX/2;
  float offsetY = 160/maxY/2;
  ucg.setColor(0, 0, 255, 0);
  for(int i=0;i<elementCount;i++){
    ucg.drawBox(y[i]*offsetY+10, x[i]*offsetX+80, 2, 2);
    delay(100);
    if(i == 15){
      break;
      }
    Serial.print(x[i]*offsetX);
    Serial.print(" ");
    Serial.println(y[i]*offsetY);
    }
  }
  

void loop() {
  lcd.clear();
  readJoystick();
  lcd.setCursor(0,0);
  lcd.print(joystickValue);
  radioTrans();
  lcd.setCursor(0,1);
  lcd.print(payloadValue);
  int length_map=ARRAY_SIZE(x);
  plotRoom(x, y, length_map);
}
