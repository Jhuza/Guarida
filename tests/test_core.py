import json
import unittest
from unittest.mock import patch
from core import DeviceState, command, Timer

def packet(state='concentracion',id='other'):
    return json.dumps(dict(v=1,state=state,id=id,source='wokwi'))

class ProtocolTests(unittest.TestCase):
    def test_invalid_command(self):
        with self.assertRaises(ValueError):command('invalid')
    def test_ack_matches_request(self):
        d=DeviceState();c=command('concentracion');d.request(c,100)
        d.receive(packet(id=c['id']),101);self.assertIsNone(d.pending);self.assertEqual(d.status(102),'Confirmado')
    def test_wrong_ack_not_confirmed(self):
        d=DeviceState();d.request(command('concentracion'),100);d.receive(packet(),101)
        self.assertIsNotNone(d.pending);self.assertEqual(d.status(110),'Sin confirmar')
    def test_wrong_state_same_id(self):
        d=DeviceState();c=command('concentracion');d.request(c,100);d.receive(packet('descanso',c['id']),101)
        self.assertIsNotNone(d.pending)
    def test_device_button_updates(self):
        d=DeviceState();d.receive(packet('descanso',''),100);self.assertEqual(d.state,'descanso')
    def test_stale_device(self):
        d=DeviceState();d.receive(packet(),100);self.assertEqual(d.status(116),'Sin señal reciente')
    def test_invalid_messages_do_not_mutate(self):
        d=DeviceState();d.receive(packet(),100)
        for raw in ('[]','bad','{"v":1,"state":"invalid"}'):
            with self.assertRaises(ValueError):d.receive(raw,101)
        self.assertEqual(d.state,'concentracion')
    def test_timer_pause_resume(self):
        with patch('core.time.monotonic',return_value=100):t=Timer();t.start(60)
        with patch('core.time.monotonic',return_value=120):t.pause()
        self.assertEqual(t.left(),40)
        with patch('core.time.monotonic',return_value=200):t.resume()
        with patch('core.time.monotonic',return_value=250):self.assertEqual(t.left(),0)

if __name__=='__main__':unittest.main()
