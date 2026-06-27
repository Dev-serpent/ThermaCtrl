/*
 SmartCooler Arduino Firmware v1.0
*/

constexpr uint8_t FAN_PIN = 8;
constexpr unsigned long SERIAL_BAUD = 115200;
constexpr size_t MAX_COMMAND_LENGTH = 64;

bool fanState = false;
String commandBuffer;

void setFan(bool state){
  fanState = state;
  digitalWrite(FAN_PIN, state ? HIGH : LOW);
}

void sendStatus(){
  Serial.print("STATUS ");
  Serial.println(fanState ? "ON" : "OFF");
}

void sendVersion(){
  Serial.println("VERSION 1.0.0");
}

void processCommand(String cmd){
  cmd.trim();
  cmd.toUpperCase();

  if(cmd=="PING"){
    Serial.println("PONG");
  }else if(cmd=="ON"){
    setFan(true);
    Serial.println("ACK ON");
  }else if(cmd=="OFF"){
    setFan(false);
    Serial.println("ACK OFF");
  }else if(cmd=="STATUS"){
    sendStatus();
  }else if(cmd=="VERSION"){
    sendVersion();
  }else if(cmd.length()){
    Serial.println("ERROR UNKNOWN_COMMAND");
  }
}

void readSerial(){
  while(Serial.available()){
    char c=Serial.read();
    if(c=='\n' || c=='\r'){
      if(commandBuffer.length()){
        processCommand(commandBuffer);
        commandBuffer="";
      }
    }else{
      if(commandBuffer.length()<MAX_COMMAND_LENGTH){
        commandBuffer+=c;
      }else{
        commandBuffer="";
        Serial.println("ERROR COMMAND_TOO_LONG");
      }
    }
  }
}

void setup(){
  pinMode(FAN_PIN,OUTPUT);
  setFan(false);
  Serial.begin(SERIAL_BAUD);
  while(!Serial){}
  Serial.println("SMARTCOOLER READY");
}

void loop(){
  readSerial();
}
