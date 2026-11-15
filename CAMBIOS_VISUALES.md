# Guarida · cubículo interactivo

## Alcance aprobado

Modelo conceptual de 3,40 × 2,80 × 2,50 m. Estructura verde pino, escritorio a la izquierda, sofá verde a la derecha, divisor opaco, fachada de vidrio inteligente y puerta corredera. Las dimensiones son una propuesta visual, no planos de fabricación.

Sin pagos ni simulación de pagos. La pantalla exterior ofrece acceso libre al prototipo; no hay autenticación ni cuentas persistentes.

## Uso

Ejecutar `python -m streamlit run app.py` con las dependencias de requirements.txt. La escena carga Babylon.js 8.0.0 desde jsDelivr y necesita Internet. `frontend/` debe acompañar a app.py al desplegar.

- Recorrer activa la cámara interior; arrastrar para mirar, WASD/flechas o botones direccionales para desplazarse. Abrir la puerta antes de entrar. Vista exterior recupera la cámara orbital.
- Las pantallas 3D y los botones alternativos abren el control exterior o interior.
- El panel interior contiene IA, privacidad, intensidad, moods, voz y reproducción de archivos de audio locales.
- La clave GROQ_API_KEY permanece en el servidor, siguiendo ACTIVAR_IA.md. Sin clave se informa que la IA está pendiente; no se inventan respuestas. El chat interior comparte historial con el asistente de Streamlit.
- Música: seleccionar un archivo de audio propio; reproducción, volumen y pausa mediante el reproductor. No se envía al servidor.

## Moods y comunicación

Bienvenida: amarillo cálido. Estudio: azul con luz superior suave. Gamer: degradado amarillo/rojo/rosado/azul. Descanso: verde. Cada cambio pasa por naranja durante tres segundos. En los últimos cinco minutos de un temporizador activo, la luminaria superior y un texto advierten el final en rojo.

La selección local permite explorar sin Wokwi y se identifica como vista local. Si MQTT está conectado, se envía el mood al dispositivo y se conserva la distinción entre solicitud y confirmación. El temporizador de Streamlit sigue esperando una confirmación coincidente. La IA y la música no viajan por MQTT.

Se añadió `gamer` al protocolo Python y al firmware; los tres botones físicos existentes conservan concentración, descanso y disponible. Es necesario actualizar el firmware del proyecto Wokwi guardado antes de probar gamer allí. El color naranja es una transición visual, no un cuarto botón físico.

## Criterios de aceptación

1. Comparar la distribución, colores y elementos con la referencia desde el exterior.
2. Abrir/cerrar la puerta y recorrer sin atravesar fachada, paredes o muebles.
3. Alternar vidrio transparente/opaco sin modificar el divisor.
4. Comprobar los cuatro moods, transición naranja y aviso rojo de finalización.
5. Enviar una pregunta desde el panel interior con clave configurada y comprobar respuesta, historial y errores.
6. Seleccionar y escuchar música, pausar y modificar volumen; probar voz donde el navegador lo permita.
7. Confirmar órdenes con Wokwi, pulsar botones físicos y detener el dispositivo para verificar pérdida de señal.
8. Ejecutar la suite automatizada y ensayar el guion de la rúbrica.

## Rúbrica conservada

Se mantienen las páginas Estudio y Descanso, tareas editables, temporizador, MQTT bidireccional, firmware, texto además de color, comandos de voz y síntesis, IA opcional y documentación académica. El nuevo componente de Streamlit permite que el panel 3D envíe preguntas a Python sin exponer credenciales.

Las pruebas históricas del repositorio no constituyen evidencia de esta versión. La conexión real con Groq, el firmware actualizado en Wokwi, la audición y las pruebas con participantes deben registrarse al realizarlas. No se atribuyen mejoras médicas ni de concentración al color o a la música.
