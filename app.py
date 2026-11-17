import json
import re
import os
import math
import time
from streamlit.components.v1 import declare_component
from pathlib import Path
import streamlit as st
from connection import Connection
from core import LABELS, Timer
from assistant_service import reply, AssistantError
from panel_events import handle_panel_event

ROOT = Path(__file__).parent
UI_BUILD = ROOT/'frontend-react'/'dist'
UI_PATH = ROOT/'frontend' if os.getenv('GUARIDA_UI') == 'legacy' or not (UI_BUILD/'index.html').exists() else UI_BUILD
room_component = declare_component('guarida_room', path=str(UI_PATH))
st.set_page_config(page_title='Guarida · JadeUI', page_icon='◉', layout='wide')
st.markdown('''<style>.stApp{background:#f4f3ec} h1{font-family:Georgia,serif;font-weight:400;letter-spacing:-.7px} .stButton button{border-radius:10px} [data-testid="stSidebar"]{background:#e9eddf} .block-container{padding-top:2.5rem} </style>''',unsafe_allow_html=True)
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

@st.fragment(run_every=1)
def connection_status():
    conn = st.session_state.get('conn')
    if not conn:
        st.caption('1. Pulsa Conectar. 2. Inicia ▶ en Wokwi.')
        return
    conn.poll()
    if conn.connected:
        st.success('Broker MQTT conectado')
        if conn.device.source == 'wokwi' and time.monotonic()-conn.device.last_seen <= 15:
            st.success('Wokwi en línea · '+LABELS.get(conn.device.state, ''))
        else:
            st.warning('Sin señal reciente de Wokwi. Inicia ▶ y comprueba el código de cubículo.')
    elif getattr(conn, 'error', ''):
        st.error(conn.error)
    elif time.monotonic()-getattr(conn, 'started_at', time.monotonic()) > 15:
        st.warning('El broker no responde todavía. Prueba el otro transporte y pulsa Conectar.')
    else:
        st.info('Conectando al broker…')
    st.caption(getattr(conn, 'endpoint', ''))
    st.caption('Canal activo: '+st.session_state.get('active_room', ''))

with st.sidebar:
    st.markdown('## ◉ GUARIDA')
    st.caption('Un espacio para comenzar.')
    with st.expander('Conexión del simulador', expanded='conn' not in st.session_state):
        host = st.text_input('Broker', 'broker.hivemq.com', disabled=True)
        room = st.text_input('Código de cubículo', 'jhuza-guarida-20261108')
        transport = st.selectbox('Transporte MQTT', ['WebSocket seguro · 8884', 'TCP · 1883'])
        st.caption('Usa el mismo código en Wokwi. Broker público: solo estados de prueba, sin objetivos ni audio.')
        if st.button('Conectar'):
            if not re.fullmatch(r'[a-zA-Z0-9_-]{3,64}', room):
                st.error('Usa 3–64 letras, números o guiones.')
            else:
                if 'conn' in st.session_state:
                    st.session_state.conn.close()
                st.session_state.conn = Connection(host, 8884 if transport.startswith('WebSocket') else 1883, room,
                                                   'websockets' if transport.startswith('WebSocket') else 'tcp')
                st.session_state.active_room = room
                st.session_state.pop('planned_timer', None)
        if st.button('Desconectar') and 'conn' in st.session_state:
            st.session_state.conn.close()
            del st.session_state.conn
            st.session_state.pop('planned_timer', None)
        connection_status()
        st.link_button('Abrir simulador Wokwi', 'https://wokwi.com/projects/480507284209602561')
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

@st.fragment(run_every=1)
def scene(zone):
    conn = st.session_state.get('conn')
    status = 'Vista local · Wokwi sin conectar'
    if conn:
        conn.poll()
        status = conn.device.status() if conn.connected else 'Sin conexión al broker'
        if conn.device.source == 'test-emulator':
            status = 'Emulador Python · ' + status
        if conn.device.status() == 'Confirmado' and conn.connected:
            st.session_state['visual_mood'] = conn.device.state
    timer = st.session_state.timer
    remaining = timer.left()
    result = room_component(
        mood=st.session_state.get('visual_mood', 'disponible'), status=status,
        ai_enabled=bool(ai_key()), chat=st.session_state.chat,
        ai_error=st.session_state.get('scene_ai_error', ''), remaining=remaining,
        ack_id=st.session_state.get('scene_event'), connected=bool(conn and conn.connected),
        device_online=bool(conn and conn.connected and conn.device.source == 'wokwi' and time.monotonic()-conn.device.last_seen<=15),
        panel_error=st.session_state.get('panel_error', ''), waiting_timer=bool(st.session_state.get('planned_timer')),
        deadline=(time.time()+remaining)*1000 if timer.deadline else None,
        key='room-'+zone, default=None)
    if handle_panel_event(result, st.session_state, conn, reply, ai_key()):
        st.rerun()

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
    st.subheader('Jade · Asistente de estudio')
    key = ai_key()
    if not key:
        st.info('Jade pendiente de activación. Puedes organizar y editar tus tareas sin ella.')
        st.caption('Configura GROQ_API_KEY en los secretos de Streamlit. No la escribas en el chat.')
        return
    st.caption('Groq recibe lo que envíes al chat y el objetivo. No se envía por MQTT. Revisa las sugerencias.')
    for message in st.session_state.chat:
        with st.chat_message(message['role']):
            st.write(message['content'])
    with st.form('assistant-chat', clear_on_submit=True):
        prompt = st.text_area('Habla con Jade', placeholder='Ayúdame a dividir mi objetivo en tres pasos', max_chars=4000)
        submit = st.form_submit_button('Enviar a Jade')
    if submit and prompt.strip():
        history = st.session_state.chat + [{'role':'user','content':prompt.strip()}]
        try:
            with st.spinner('Jade está preparando una respuesta…'):
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
    scene('study')
    left,right=st.columns([.4,1])
    with left:
        st.subheader('Tu próxima meta')
        st.write('Prepara un objetivo concreto y guarda los pasos que quieres completar. El panel del cubículo acompaña tu sesión.')
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
    scene('rest')
    left,right=st.columns([.4,1])
    with left:
        st.subheader('Una pausa a tu ritmo')
        st.write('Ajusta la luz, escucha tu música y date un momento antes de volver.')
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
    assistant_panel()

st.navigation([st.Page(study,title='Estudio',icon='📖'),st.Page(rest,title='Descanso',icon='☕')]).run()
