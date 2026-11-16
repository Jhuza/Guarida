# Guarida · iteración de escritorio, 16 de noviembre de 2026

Entrega prevista: jueves 19 de noviembre, entre 6:00 y 15:00 (Colombia). Se prioriza computador. No se incluyen pagos ni simulaciones de pago. El inicio de sesión con cuentas sigue pendiente y no se presenta como implementado.

## Arquitectura y ejecución

React organiza el panel y Vite genera los archivos que sirve Streamlit. Babylon.js conserva la escena 3D. Python conserva MQTT, temporizador, tareas y adaptador de IA. Node.js se usa para compilar; no requiere otro servidor en producción.

La aplicación carga `frontend-react/dist` si existe. Para volver a la interfaz anterior, establece `GUARIDA_UI=legacy` antes de iniciar Streamlit. No se eliminó `frontend/`.

Desde la raíz del repositorio:

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Para editar y recompilar la interfaz (Node >=22.12):

```powershell
cd frontend-react
npm ci
npm test
npm run build
```

Se incluye `dist` para que Streamlit Cloud pueda servir la interfaz sin instalar Node. La rama de trabajo es `mejora/react-vite`. Por solicitud del autor, esta versión y las mejoras de MQTT se publicaron en `main` el 16 de noviembre; el despliegue público debe comprobarse tras su reinicio.

## Funcionalidad y diseño

- Panel con Ambiente, Asistente y Sesión; navegación exterior/interior, puerta corredera, privacidad del vidrio, intensidad y archivo de música local.
- Bienvenida amarilla, estudio azul, ocio multicolor, descanso verde; transición naranja y aviso rojo en los últimos cinco minutos de una sesión activa.
- Inicio de temporizador condicionado a confirmación del dispositivo. Los eventos del panel se validan y los duplicados recientes se descartan.
- El estado distingue conexión al broker de presencia reciente del dispositivo. No se muestra una conexión MQTT como prueba suficiente de Wokwi activo.
- Dimensiones propuestas de planta: 3,40 × 2,80 m. Son una hipótesis del prototipo, no medidas verificadas de la referencia ni un plano constructivo.
- Escena cargada por separado, recursos Babylon empaquetados, materiales LED compartidos y render suspendido cuando la página queda oculta.

## Evidencia y límites

29 pruebas Python y 3 pruebas JavaScript aprobadas; compilación Vite aprobada. Las pruebas de IA emplean un adaptador simulado, no acreditan una respuesta real de Groq. Se completaron seis comprobaciones de red con emulador Python explícito; esto no sustituye Wokwi.

En navegador local se comprobó carga de React/Babylon, cambio a Ocio y apertura de puerta. Se corrigió la superposición del cubículo sobre el título en una ventana de escritorio estrecha.

La sesión anterior de Wokwi compiló el firmware y mostró arranque/heartbeat, pero se perdió la sesión de navegador antes de completar y registrar el recorrido integrado. Sigue pendiente repetir gamer, confirmación de temporizador, botón físico y desconexión con Wokwi real, y guardar el firmware actualizado en el proyecto público.

No se ha medido todavía la carga en frío ni la fluidez en el computador de presentación. El tamaño del archivo principal de React no representa el tamaño total de la aplicación. El modelo sigue siendo procedural y necesita revisión visual contra la imagen original; no se afirma fidelidad final.

## Cierre antes de entregar

1. 16–17: revisar referencia visual y decisiones de UI/UX; completar ensayo real Wokwi y respuesta de IA. La clave Groq se configura solo en secretos del servidor, nunca en el chat ni el código del navegador.
2. 17–18: prueba de voz/audio con el usuario, usabilidad con compañeros y correcciones. Conservar evidencia real; no inventar resultados de participantes.
3. 18: ensayo completo y cronometrado, comprobar acceso del evaluador al repositorio, actualizar informe y congelar versión verificada.
4. 19: abrir aplicación, comprobar red/IA/Wokwi y presentar dentro de la franja acordada.

La matriz `RUBRICA_Y_PRUEBAS.md` sigue siendo la referencia académica. Los cambios de interfaz preservan sus funciones, pero no equivalen a certificar todos los criterios: faltan participantes, ensayo, IA real y revisión del informe.
