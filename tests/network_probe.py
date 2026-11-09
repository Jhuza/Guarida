"""Real broker roundtrip with explicit Python emulator, NOT Wokwi validation."""
import json,time,uuid
import paho.mqtt.client as mqtt
from connection import Connection

room='test-'+uuid.uuid4().hex
app=Connection('broker.hivemq.com',1883,room)
device=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,client_id='test-device-'+uuid.uuid4().hex)
def on_connect(c,u,f,r,p):c.subscribe('guarida/'+room+'/command',qos=1)
def on_message(c,u,m):
    d=json.loads(m.payload);d['source']='test-emulator'
    c.publish('guarida/'+room+'/state',json.dumps(d),qos=1)
device.on_connect=on_connect;device.on_message=on_message
try:
 device.connect('broker.hivemq.com',1883,30);device.loop_start()
 deadline=time.monotonic()+15
 while not app.connected and time.monotonic()<deadline:time.sleep(.1)
 time.sleep(1)
 for s in ('concentracion','descanso','disponible'):
    app.send(s);deadline=time.monotonic()+10
    while app.device.pending and time.monotonic()<deadline:app.poll();time.sleep(.1)
    assert app.device.pending is None and app.device.state==s,(s,app.device.status())
    print('PASS broker TCP command + matching confirmation:',s)
 device.publish('guarida/'+room+'/state',json.dumps(dict(v=1,state='descanso',id='',source='test-emulator')),qos=1)
 time.sleep(1);app.poll();assert app.device.state=='descanso'
 print('PASS independent device event -> app')
 ws=Connection('broker.hivemq.com',8884,room,'websockets')
 try:
    deadline=time.monotonic()+15
    while not ws.connected and time.monotonic()<deadline:time.sleep(.1)
    assert ws.connected,'WSS unavailable'
    ws.send('disponible');deadline=time.monotonic()+10
    while ws.device.pending and time.monotonic()<deadline:ws.poll();time.sleep(.1)
    assert ws.device.pending is None
    print('PASS secure WebSocket -> TCP device -> matching confirmation')
 finally:ws.close()
finally:
 app.close();device.disconnect();device.loop_stop()
