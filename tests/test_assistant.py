import io
import json
import unittest
import urllib.error
from unittest.mock import patch
from assistant_service import reply, AssistantError

class AssistantTests(unittest.TestCase):
    def test_no_key_no_request(self):
        with patch('urllib.request.urlopen') as call:
            with self.assertRaises(AssistantError): reply('', [])
            call.assert_not_called()

    def test_success_and_bounded_history(self):
        response = io.BytesIO(json.dumps({'choices':[{'message':{'content':'Plan de estudio'}}]}).encode())
        with patch('urllib.request.urlopen', return_value=response) as call:
            result = reply('test-key', [{'role':'user','content':'hola'}]*30, 'Repasar')
        self.assertEqual(result, 'Plan de estudio')
        payload = json.loads(call.call_args.args[0].data)
        self.assertEqual(len(payload['messages']), 14)
        self.assertNotIn('test-key', str(payload))

    @patch.dict('os.environ', {}, clear=True)
    def test_jade_uses_current_model_and_final_answer_only(self):
        response = io.BytesIO(json.dumps({'choices':[{'message':{'content':'Soy Jade.', 'reasoning':'internal'}}]}).encode())
        with patch('urllib.request.urlopen', return_value=response) as call:
            self.assertEqual(reply('test-key', [{'role':'user','content':'¿Quién eres?'}]), 'Soy Jade.')
        payload = json.loads(call.call_args.args[0].data)
        self.assertEqual(payload['model'], 'openai/gpt-oss-120b')
        self.assertFalse(payload['include_reasoning'])
        self.assertIn('JadeUI', payload['messages'][0]['content'])

    def test_incomplete_generation_is_not_presented_as_success(self):
        response = io.BytesIO(json.dumps({'choices':[{'finish_reason':'length','message':{'content':'Parcial'}}]}).encode())
        with patch('urllib.request.urlopen', return_value=response):
            with self.assertRaisesRegex(AssistantError, 'límite'):
                reply('test-key', [])

    def test_errors_are_safe_and_actionable(self):
        for error in (urllib.error.HTTPError('url',429,'secret',{},None),
                      urllib.error.URLError('secret'), TimeoutError('secret')):
            with patch('urllib.request.urlopen', side_effect=error):
                with self.assertRaises(AssistantError) as ctx: reply('private', [])
                self.assertNotIn('secret', str(ctx.exception))

    def test_invalid_response(self):
        with patch('urllib.request.urlopen', return_value=io.BytesIO(b'{}')):
            with self.assertRaises(AssistantError): reply('test', [])
