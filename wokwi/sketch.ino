#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

const char* ROOM = "jhuza-guarida-20261108";
const char* BROKER = "broker.hivemq.com";
WiFiClient net;
PubSubClient mqtt(net);
Adafruit_SSD1306 display(128,64,&Wire,-1);
String prefix, currentState="disponible", lastId="", bootId;
unsigned long lastConnect=0,lastBeat=0;
const int pins[]={25,26,27};
const char* states[]={"concentracion","descanso","disponible"};
bool stable[]={HIGH,HIGH,HIGH},rawPrev[]={HIGH,HIGH,HIGH};
unsigned long changedAt[]={0,0,0};
void render(){
 display.clearDisplay(); display.setTextColor(SSD1306_WHITE);display.setTextSize(1);
 display.setCursor(0,0);display.println("GUARIDA / AURORA");display.println("---------------------");
 display.println(currentState);display.println();display.println(mqtt.connected()?"MQTT conectado":"MQTT desconectado");display.display();
}
void publishState(String id="",String cause="heartbeat"){
 JsonDocument d;d["v"]=1;d["id"]=id;d["state"]=currentState;d["source"]="wokwi";d["cause"]=cause;d["boot"]=bootId;d["uptime"]=millis();
 char buffer[384];serializeJson(d,buffer,sizeof(buffer));mqtt.publish((prefix+"/state").c_str(),buffer,false);Serial.println(buffer);
}
void received(char* topic,byte* payload,unsigned int length){
 if(length>384)return;
 JsonDocument d;if(deserializeJson(d,payload,length))return;
 if(d["v"].as<int>()!=1||!d["id"].is<String>()||!d["state"].is<String>())return;
 String id=d["id"].as<String>(),s=d["state"].as<String>();
 if(id.length()<1||id.length()>64)return;
 if(s!="concentracion"&&s!="descanso"&&s!="disponible")return;
 if(id==lastId){publishState(id,"duplicate");return;}
 currentState=s;lastId=id;render();publishState(id,"command");
}
void setup(){
 Serial.begin(115200);bootId=String((uint32_t)esp_random(),HEX);prefix=String("guarida/")+ROOM;
 Wire.begin(21,22);display.begin(SSD1306_SWITCHCAPVCC,0x3c);
 for(int p:pins)pinMode(p,INPUT_PULLUP);
 WiFi.begin("Wokwi-GUEST","",6);mqtt.setServer(BROKER,1883);mqtt.setCallback(received);mqtt.setBufferSize(512);mqtt.setSocketTimeout(2);render();
}
void loop(){
 unsigned long now=millis();
 if(WiFi.status()==WL_CONNECTED&&!mqtt.connected()&&(lastConnect==0||now-lastConnect>3000)){
  lastConnect=now;String cid=String("guarida-wokwi-")+bootId;
  if(mqtt.connect(cid.c_str())){mqtt.subscribe((prefix+"/command").c_str(),1);publishState("","boot");}render();
 }
 mqtt.loop();
 for(int i=0;i<3;i++){
  bool raw=digitalRead(pins[i]);if(raw!=rawPrev[i]){changedAt[i]=now;rawPrev[i]=raw;}
  if(now-changedAt[i]>40&&stable[i]!=raw){stable[i]=raw;if(raw==LOW){currentState=states[i];render();publishState("","button");}}
 }
 if(mqtt.connected()&&now-lastBeat>4000){lastBeat=now;render();publishState();}
}
