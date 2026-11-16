"""Validated panel actions, independent of Streamlit rendering."""
from core import LABELS
from assistant_service import AssistantError


def handle_panel_event(event, state, conn, ai_reply, ai_key):
    """Process each event once. Return True when a fresh event was consumed."""
    if not isinstance(event, dict):
        return False
    event_id = event.get('id')
    if not isinstance(event_id, str) or not 1 <= len(event_id) <= 80:
        return False
    if event_id == state.get('scene_event') or event_id in state.get('panel_event_ids', []):
        return False
    state['scene_event'] = event_id
    state['panel_event_ids'] = (state.get('panel_event_ids', []) + [event_id])[-64:]
    state['panel_error'] = ''
    action = event.get('action')
    try:
        if action == 'mood':
            mood = event.get('mood')
            if not isinstance(mood, str) or mood not in LABELS:
                raise ValueError('Ambiente no válido.')
            state['visual_mood'] = mood
            state.pop('planned_timer', None)
            if conn and conn.connected:
                conn.send(mood)
        elif action == 'chat':
            prompt = event.get('prompt')
            if not isinstance(prompt, str) or not prompt.strip() or len(prompt) > 4000:
                raise ValueError('Escribe una pregunta de hasta 4000 caracteres.')
            history = state.get('chat', []) + [{'role': 'user', 'content': prompt.strip()}]
            try:
                answer = ai_reply(ai_key, history, state.get('goal', ''))
                state['chat'] = (history + [{'role': 'assistant', 'content': answer}])[-12:]
                state['scene_ai_error'] = ''
            except AssistantError as exc:
                state['scene_ai_error'] = str(exc)
        elif action == 'session_start':
            minutes, mood = event.get('minutes'), event.get('mood')
            if type(minutes) is not int or not 1 <= minutes <= 60 or mood not in ('concentracion', 'descanso', 'gamer'):
                raise ValueError('Selecciona un ambiente y entre 1 y 60 minutos.')
            if not conn or not conn.connected:
                raise ValueError('Conecta el simulador para iniciar una sesión confirmada.')
            state.pop('planned_timer', None)
            conn.send(mood)
            state['planned_timer'] = dict(id=conn.device.pending['id'], seconds=minutes*60, state=mood)
        elif action == 'session_pause':
            state['timer'].pause()
            state.pop('planned_timer', None)
        elif action == 'session_resume':
            state['timer'].resume()
        elif action == 'session_end':
            state['timer'].start(0)
            state['timer'].pause()
            state.pop('planned_timer', None)
        else:
            raise ValueError('Esta acción no está disponible.')
    except (ValueError, RuntimeError) as exc:
        state['panel_error'] = str(exc)
    return True
