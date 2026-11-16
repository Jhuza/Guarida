import unittest
from unittest.mock import Mock
from core import Timer, DeviceState, command
from panel_events import handle_panel_event
from assistant_service import AssistantError

class Connection:
    connected = True
    def __init__(self):
        self.device = DeviceState()
        self.calls = 0
    def send(self, mood):
        self.calls += 1
        self.device.request(command(mood))

class PanelTests(unittest.TestCase):
    def setUp(self):
        self.state = {'timer': Timer(), 'chat': [], 'goal': 'Aprender'}
        self.conn = Connection()
        self.reply = Mock(return_value='Primer paso')
    def act(self, action, **data):
        return handle_panel_event(dict(id='event-'+action, action=action, **data), self.state, self.conn, self.reply, '')
    def test_start_waits_for_device(self):
        self.act('session_start', minutes=25, mood='concentracion')
        self.assertIsNone(self.state['timer'].deadline)
        self.assertEqual(self.state['planned_timer']['id'],self.conn.device.pending['id'])
        self.assertEqual(self.state['planned_timer']['seconds'],1500)
    def test_duplicate_start_not_republished(self):
        self.act('session_start', minutes=25, mood='gamer')
        self.assertFalse(self.act('session_start', minutes=25, mood='gamer'))
        self.assertEqual(self.conn.calls,1)
    def test_bad_duration_does_not_publish(self):
        for value in [True,0,-1,61,'25',{},None]:
            self.state.pop('scene_event',None)
            self.state.pop('panel_event_ids',None)
            self.act('session_start',minutes=value,mood='gamer')
            self.assertTrue(self.state['panel_error'])
        self.assertEqual(self.conn.calls,0)
    def test_offline_cannot_start(self):
        self.conn.connected=False
        self.act('session_start',minutes=25,mood='gamer')
        self.assertNotIn('planned_timer',self.state)
        self.assertIsNone(self.state['timer'].deadline)
    def test_replayed_event_after_another_action_is_ignored(self):
        self.act('session_start',minutes=25,mood='gamer')
        self.act('session_end')
        self.assertFalse(self.act('session_start',minutes=25,mood='gamer'))
        self.assertNotIn('planned_timer',self.state)
        self.assertEqual(self.conn.calls,1)
    def test_end_cancels_pending_start(self):
        self.act('session_start',minutes=25,mood='gamer')
        self.act('session_end')
        self.assertNotIn('planned_timer',self.state)
        self.assertEqual(self.state['timer'].left(),0)
    def test_mood_change_cancels_pending_start(self):
        self.act('session_start',minutes=25,mood='concentracion')
        self.act('mood',mood='descanso')
        self.assertNotIn('planned_timer',self.state)
    def test_ai_failure_preserves_history_and_acknowledges_event(self):
        self.state['chat']=[{'role':'assistant','content':'Hola'}]
        self.reply.side_effect=AssistantError('Sin conexión')
        self.act('chat',prompt='Hola')
        self.assertEqual(len(self.state['chat']),1)
        self.assertEqual(self.state['scene_ai_error'],'Sin conexión')
        self.assertEqual(self.state['scene_event'],'event-chat')
    def test_pause_cancels_pending_and_resume_preserves_time(self):
        self.state['timer'].start(60)
        self.state['planned_timer']={'id':'older'}
        self.act('session_pause')
        self.assertIsNone(self.state['timer'].deadline)
        self.assertNotIn('planned_timer',self.state)
        self.act('session_resume')
        self.assertGreater(self.state['timer'].left(),58)

if __name__ == '__main__': unittest.main()
