import unittest
import json
from streamlit.testing.v1 import AppTest
from core import DeviceState, command

class FakeConnection:
    connected=True
    def __init__(self): self.device=DeviceState()
    def poll(self): pass
    def send(self,state): self.device.request(command(state))

class AppTests(unittest.TestCase):
    def test_goal_and_empty_input(self):
        a=AppTest.from_file('../app.py').run(timeout=30)
        self.assertEqual(len(a.exception),0)
        next(b for b in a.button if b.label=='Preparar mi sesión').click().run()
        self.assertTrue(any('Escribe un objetivo' in w.value for w in a.warning))
        next(t for t in a.text_input if t.label=='Objetivo de la sesión').set_value('Repasar interfaces').run()
        next(b for b in a.button if b.label=='Preparar mi sesión').click().run()
        self.assertEqual(len(a.checkbox),3)
        self.assertEqual(len(a.exception),0)
    def test_offline_request_is_not_success(self):
        a=AppTest.from_file('../app.py').run(timeout=30)
        next(b for b in a.button if b.label=='Iniciar concentración').click().run()
        self.assertTrue(any('Conecta' in w.value for w in a.warning))
        self.assertIsNone(a.session_state['timer'].deadline)
        self.assertEqual(len(a.exception),0)

    def test_edit_tasks_and_reset_progress(self):
        a=AppTest.from_file('../app.py').run(timeout=30)
        next(t for t in a.text_input if t.label=='Objetivo de la sesión').set_value('Repasar').run()
        next(b for b in a.button if b.label=='Preparar mi sesión').click().run()
        a.checkbox[0].check().run()
        self.assertTrue(a.session_state['completed']['0'])
        next(t for t in a.text_area if t.label=='Una tarea por línea').set_value('Resolver tres preguntas\nRevisar errores').run()
        next(b for b in a.button if b.label=='Guardar tareas').click().run()
        self.assertEqual([c.label for c in a.checkbox],['Resolver tres preguntas','Revisar errores'])
        self.assertFalse(a.checkbox[0].value)
        self.assertEqual(len(a.exception),0)

    def test_timer_waits_for_matching_device_ack(self):
        a=AppTest.from_file('../app.py').run(timeout=30)
        conn=FakeConnection()
        a.session_state['conn']=conn
        a.run()
        next(b for b in a.button if b.label=='Iniciar concentración').click().run()
        self.assertIsNone(a.session_state['timer'].deadline)
        pending=dict(conn.device.pending)
        conn.device.receive(json.dumps(dict(v=1,id='wrong',state='concentracion',source='wokwi')))
        a.run()
        self.assertIsNone(a.session_state['timer'].deadline)
        conn.device.receive(json.dumps({**pending,'source':'wokwi'}))
        a.run()
        self.assertGreater(a.session_state['timer'].left(),1490)
        self.assertEqual(len(a.exception),0)

    def test_terminate_cancels_waiting_timer(self):
        a=AppTest.from_file('../app.py').run(timeout=30)
        conn=FakeConnection()
        a.session_state['conn']=conn
        a.run()
        next(b for b in a.button if b.label=='Iniciar concentración').click().run()
        pending=dict(conn.device.pending)
        next(b for b in a.button if b.label=='Terminar').click().run()
        conn.device.receive(json.dumps({**pending,'source':'wokwi'}))
        a.run()
        self.assertIsNone(a.session_state['timer'].deadline)

if __name__=='__main__':unittest.main()

