import json
import re
import os
import math
from pathlib import Path
import streamlit as st
from connection import Connection
from core import LABELS, Timer
from assistant_service import reply, AssistantError

ROOT = Path(__file__).parent
st.set_page_config(page_title='Guarida · Aurora', page_icon='◉', layout='wide')
st.markdown('''<style>.stApp{background:radial-gradient(ellipse at 85% 0%,#132a47,transparent 55%),#05070b} h1{font-family:Georgia,serif;font-weight:400} .stButton button{border-radius:14px} [data-testid="stSidebar"]{background:#0b111c} </style>''',unsafe_allow_html=True)
if 'timer' not in st.session_state:
    st.session_state.timer = Timer()
    st.session_state.tasks = []
    st.session_state.goal = ''
    st.session_state.completed = {}
st.session_state.setdefault('completed', {})
st.session_state.setdefault('chat', [])

def ai_key():
    key = os.getenv('GROQ_API_KEY', '')
    if key:
        return key
    try:
        return st.secrets.get('GROQ_API_KEY', '')
    except (FileNotFoundError, st.errors.StreamlitSecretNotFoundError):
        return ''

with st.sidebar:
    st.markdown('## ◉ GUARIDA')
    st.caption('Un espacio para comenzar.')
    with st.expander('Conexión del simulador', expanded='conn' not in st.session_state):
        host = st.text_input('Broker', 'broker.hivemq.com', disabled=True)
        room = st.text_input('Código de cubículo', 'jhuza-guarida-20261108')
        st.caption('Usa el mismo código en Wokwi. Broker público: solo estados de prueba, sin objetivos ni audio.')
        if st.button('Conectar'):
            if not re.fullmatch(r'[a-zA-Z0-9_-]{3,64}', room):
                st.error('Usa 3–64 letras, números o guiones.')
            else:
                if 'conn' in st.session_state:
                    st.session_state.conn.close()
                st.session_state.conn = Connection(host, 1883, room)
                st.session_state.active_room = room
                st.session_state.pop('planned_timer', None)
        if st.button('Desconectar') and 'conn' in st.session_state:
            st.session_state.conn.close()
            del st.session_state.conn
            st.session_state.pop('planned_timer', None)
    st.caption('Prototipo · hardware simulado')

def send(state):
    try:
        st.session_state.conn.send(state)
        st.session_state.pop('planned_timer', None)
        return True
    except (RuntimeError, AttributeError) as exc:
        st.warning(str(exc) if isinstance(exc, RuntimeError) else 'Conecta el simulador primero.')
        return False

@st.fragment(run_every=1)
def live_status():
    conn = st.session_state.get('conn')
    if conn:
        conn.poll()
        dev = conn.device
        state_status = dev.status() if conn.connected else 'Sin conexión al broker'
        planned = st.session_state.get('planned_timer')
        if planned and conn.connected and not dev.pending:
            if dev.state == planned['state'] and dev.status() == 'Confirmado' and any(e.get('id') == planned['id'] and e['state'] == planned['state'] for e in dev.events):
                st.session_state.timer.start(planned['seconds'])
                del st.session_state.planned_timer
        st.caption(('MQTT conectado' if conn.connected else 'Conectando o sin conexión')+' · '+state_status)
        st.write('Estado del dispositivo: **'+LABELS.get(dev.state, 'Aún no confirmado')+'**')
        if dev.source == 'test-emulator':
            st.warning('Dispositivo de prueba Python; no es Wokwi.')
        if dev.pending:
            st.caption('Solicitado: '+LABELS[dev.pending['state']])
        with st.expander('Evidencia de mensajes'):
            st.json(dev.events[-5:])
            st.download_button('Descargar mensajes',json.dumps(dev.events,ensure_ascii=False,indent=2),'guarida-mensajes.json','application/json')
    else:
        st.info('Conecta MQTT y ejecuta Wokwi para confirmar estados.')

def scene(zone):
    cfg = {'room': st.session_state.get('active_room',room), 'zone':zone, 'host':host}
    html = (ROOT/'scene.html').read_text(encoding='utf-8').replace('__CONFIG__',json.dumps(cfg).replace('<','\\u003c'))
    # Isolated iframe keeps Babylon and audio independent of Python dependencies.
    st.iframe(html, height=560, alt='Guarida: ambientes de estudio y descanso en 3D')

@st.fragment(run_every=1)
def timer_panel():
    timer = st.session_state.timer
    left = math.ceil(timer.left())
    st.metric('Tiempo restante', f'{left//60:02d}:{left%60:02d}')
    if timer.deadline and left == 0:
        st.info('Terminó el bloque. Decide si descansas o continúas.')
    a,b,c = st.columns(3)
    if a.button('Pausar'): timer.pause()
    if b.button('Continuar'): timer.resume()
    if c.button('Terminar'):
        timer.start(0)
        timer.pause()
        st.session_state.pop('planned_timer', None)

def assistant_panel():
    st.subheader('Asistente de estudio')
    key = ai_key()
    if not key:
        st.info('IA pendiente de activación. Puedes organizar y editar tus tareas sin ella.')
        st.caption('Configura GROQ_API_KEY en los secretos de Streamlit. No la escribas en el chat.')
        return
    st.caption('Groq recibe lo que envíes al chat y el objetivo. No se envía por MQTT. Revisa las sugerencias.')
    for message in st.session_state.chat:
        with st.chat_message(message['role']):
            st.write(message['content'])
    with st.form('assistant-chat', clear_on_submit=True):
        prompt = st.text_area('Habla con Guarida', placeholder='Ayúdame a dividir mi objetivo en tres pasos', max_chars=4000)
        submit = st.form_submit_button('Enviar a la IA')
    if submit and prompt.strip():
        history = st.session_state.chat + [{'role':'user','content':prompt.strip()}]
        try:
            with st.spinner('Guarida está preparando una respuesta…'):
                answer = reply(key, history, st.session_state.goal)
            st.session_state.chat = (history + [{'role':'assistant','content':answer}])[-12:]
            st.rerun()
        except AssistantError as exc:
            st.error(str(exc))
    if st.button('Limpiar conversación'):
        st.session_state.chat = []
        st.rerun()

def study():
    st.caption('01 / ESTUDIO')
    st.title('Tu siguiente paso empieza aquí.')
    left,right=st.columns([1.55,1])
    with left: scene('study')
    with right:
        st.subheader('¿Qué quieres lograr hoy?')
        goal=st.text_input('Objetivo de la sesión',value=st.session_state.goal,placeholder='Preparar el parcial de interfaces')
        minutes=st.slider('Minutos de estudio',1,60,25)
        if st.button('Preparar mi sesión',type='primary'):
            if goal.strip():
                st.session_state.goal=goal.strip()
                st.session_state.tasks=['Definir el primer paso de: '+goal.strip(),'Trabajar en ese paso y anotar dudas','Revisar qué quedó resuelto y qué falta']
                st.session_state.completed = {}
                st.session_state.chat = []
                for k in list(st.session_state):
                    if k.startswith('task-'): del st.session_state[k]
            else: st.warning('Escribe un objetivo concreto.')
        st.caption('Lista inicial por reglas, editable. La IA opcional puede ayudarte a concretarla.')
        for i,task in enumerate(st.session_state.tasks):
            st.session_state.completed[str(i)] = st.checkbox(task,value=st.session_state.completed.get(str(i),False),key=f'task-{st.session_state.goal}-{i}')
        if st.session_state.tasks:
            with st.expander('Ajustar mis tareas'):
                revised = st.text_area('Una tarea por línea','\n'.join(st.session_state.tasks))
                if st.button('Guardar tareas'):
                    tasks = [t.strip() for t in revised.splitlines() if t.strip()]
                    if 1 <= len(tasks) <= 8:
                        st.session_state.tasks=tasks
                        st.session_state.completed={}
                        for k in list(st.session_state):
                            if k.startswith('task-'): del st.session_state[k]
                        st.rerun()
                    else: st.warning('Escribe entre una y ocho tareas.')
            st.download_button('Guardar resumen de sesión',json.dumps({'objetivo':st.session_state.goal,'tareas':st.session_state.tasks,'completadas':st.session_state.completed},ensure_ascii=False,indent=2),'guarida-sesion.json','application/json')
        if st.button('Iniciar concentración'):
            if send('concentracion'):
                st.session_state.planned_timer = dict(id=st.session_state.conn.device.pending['id'],seconds=minutes*60,state='concentracion')
        if st.button('Marcar disponible'): send('disponible')
        timer_panel()
        live_status()
    assistant_panel()

def rest():
    st.caption('02 / DESCANSO')
    st.title('Haz espacio para una pausa.')
    left,right=st.columns([1.55,1])
    with left: scene('rest')
    with right:
        st.write('Levántate, cambia de postura y mira lejos de la pantalla.')
        minutes=st.slider('Minutos de descanso',1,20,5)
        if st.button('Iniciar descanso',type='primary'):
            if send('descanso'):
                st.session_state.planned_timer = dict(id=st.session_state.conn.device.pending['id'],seconds=minutes*60,state='descanso')
        if st.button('Volver a concentración'): send('concentracion')
        timer_panel()
        st.caption('El sonido ambiental se activa desde la escena. Es una preferencia, no una intervención terapéutica.')
        live_status()

st.navigation([st.Page(study,title='Estudio',icon='📖'),st.Page(rest,title='Descanso',icon='☕')]).run()
