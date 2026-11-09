"""Protocol and timer logic, independent from UI and network."""
import json
import time
import uuid

STATES = ('concentracion', 'descanso', 'disponible')
LABELS = dict(zip(STATES, ('Concentración', 'Descanso', 'Disponible')))

def command(state):
    if state not in STATES:
        raise ValueError('Estado no permitido')
    return {'v': 1, 'id': uuid.uuid4().hex, 'state': state}

def parse_state(raw):
    data = json.loads(raw)
    if not isinstance(data, dict) or data.get('v') != 1 or data.get('state') not in STATES:
        raise ValueError('Mensaje no válido')
    if data.get('source') not in ('wokwi', 'test-emulator'):
        raise ValueError('Origen no válido')
    return data

class DeviceState:
    def __init__(self):
        self.state = None
        self.source = None
        self.last_seen = 0
        self.pending = None
        self.sent_at = 0
        self.events = []

    def request(self, data, now=None):
        self.pending = data
        self.sent_at = time.monotonic() if now is None else now

    def receive(self, raw, now=None):
        data = parse_state(raw)
        self.state, self.source = data['state'], data['source']
        self.last_seen = time.monotonic() if now is None else now
        if self.pending and data.get('id') == self.pending['id'] and data['state'] == self.pending['state']:
            self.pending = None
        self.events = (self.events + [data])[-30:]

    def status(self, now=None):
        now = time.monotonic() if now is None else now
        if self.pending:
            return 'Sin confirmar' if now - self.sent_at > 8 else 'Esperando confirmación'
        return 'Sin señal reciente' if not self.last_seen or now-self.last_seen > 15 else 'Confirmado'

class Timer:
    def __init__(self):
        self.remaining = 0
        self.deadline = None
    def start(self, seconds):
        self.remaining = seconds
        self.deadline = time.monotonic() + seconds
    def left(self):
        return max(0, self.remaining if self.deadline is None else self.deadline-time.monotonic())
    def pause(self):
        self.remaining = self.left()
        self.deadline = None
    def resume(self):
        if self.remaining > 0 and self.deadline is None:
            self.deadline = time.monotonic()+self.remaining
