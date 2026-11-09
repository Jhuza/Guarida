import json
import queue
import uuid
import paho.mqtt.client as mqtt
from core import DeviceState, command

class Connection:
    def __init__(self, host, port, room, transport='tcp'):
        self.device = DeviceState()
        self.inbox = queue.Queue(maxsize=200)
        self.connected = False
        self.error = ''
        self.prefix = 'guarida/'+room
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id='guarida-app-'+uuid.uuid4().hex[:12], transport=transport)
        if transport == 'websockets':
            self.client.ws_set_options(path='/mqtt')
            self.client.tls_set()
        self.client.on_connect = self._connect
        self.client.on_disconnect = lambda *args: setattr(self, 'connected', False)
        self.client.on_message = self._message
        self.client.connect_async(host, port, 30)
        self.client.loop_start()
    def _connect(self, client, userdata, flags, reason, properties):
        self.connected = not reason.is_failure
        if self.connected:
            client.subscribe(self.prefix+'/state', qos=1)
    def _message(self, client, userdata, msg):
        if msg.retain:
            return # Retained state is not evidence of a live device.
        try:
            self.inbox.put_nowait(msg.payload.decode())
        except (queue.Full, UnicodeDecodeError):
            pass
    def poll(self):
        while not self.inbox.empty():
            try:
                self.device.receive(self.inbox.get_nowait())
            except (ValueError, TypeError):
                self.error = 'Se ignoró un mensaje inválido.'
    def send(self, state):
        if not self.connected:
            raise RuntimeError('Conecta primero con MQTT.')
        data = command(state)
        result = self.client.publish(self.prefix+'/command', json.dumps(data), qos=1, retain=False)
        if result.rc != mqtt.MQTT_ERR_SUCCESS:
            raise RuntimeError('No se pudo enviar la solicitud.')
        self.device.request(data)
    def close(self):
        self.client.disconnect()
        self.client.loop_stop()
