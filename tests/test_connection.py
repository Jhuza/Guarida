import unittest
from unittest.mock import Mock, patch
from connection import Connection


class ConnectionTests(unittest.TestCase):
    @patch('connection.mqtt.Client')
    def test_secure_transport_and_recovery_status(self, factory):
        conn = Connection('broker.hivemq.com', 8884, 'demo-room', 'websockets')
        client = factory.return_value
        client.ws_set_options.assert_called_once_with(path='/mqtt')
        client.tls_set.assert_called_once_with()
        conn._connect_fail(client, None)
        self.assertFalse(conn.connected)
        self.assertIn('alcanzar', conn.error)
        conn._connect(client, None, None, Mock(is_failure=False), None)
        self.assertTrue(conn.connected)
        self.assertEqual(conn.error, '')
        client.subscribe.assert_called_once_with('guarida/demo-room/state', qos=1)
        conn._disconnect(client, None, None, Mock(is_failure=True), None)
        self.assertFalse(conn.connected)
        self.assertIn('Reconectando', conn.error)

    @patch('connection.mqtt.Client')
    def test_retained_state_never_proves_device_is_online(self, factory):
        conn = Connection('broker.hivemq.com', 1883, 'demo-room')
        conn._message(None, None, Mock(retain=True, payload=b'{"v":1,"state":"gamer","source":"wokwi"}'))
        conn.poll()
        self.assertIsNone(conn.device.state)
