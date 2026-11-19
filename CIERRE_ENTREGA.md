# Guarida · estado de cierre

Fecha de revisión: 19 de noviembre de 2026. Presentación: jueves 19 de noviembre, entre 6:00 y 15:00, desde computador.

## Enlaces

- Aplicación: https://guaridastudio.streamlit.app/
- Circuito guardado: https://wokwi.com/projects/480507284209602561
- Código: https://github.com/Jhuza/Guarida

## Comprobado

La app pública carga React y Babylon después del reinicio y de despertar el servicio. El circuito guardado contiene Estudio, Descanso, Bienvenida y Ocio. La conexión de Streamlit usa MQTT sobre WebSocket seguro, mientras el ESP32 de Wokwi usa TCP hacia el mismo broker.

Prueba pública realizada con arranque Wokwi `1daec287`:

| Acción | Evidencia |
|---|---|
| App envía Ocio | Wokwi respondió `gamer`, causa `command`, id `35d4bff07ffd481dbf267e320396faa2`; app mostró Confirmado. |
| Botón verde de Wokwi | Publicó `descanso`, causa `button`, uptime 18467; app cambió a Descanso. |
| Inicio de sesión | Respuesta id `caba56af021d42c58a8454574e516097`; contador público observado en curso, después se terminó la prueba. |
| Detener Wokwi | La app pública mostró «Sin señal reciente» y mantuvo «Broker MQTT conectado». Se reinició el circuito al terminar el ensayo. |

El informe se actualizó a la arquitectura real: React no conecta directamente a MQTT; transmite acciones al servidor Python. Node/Vite se utiliza para compilar, no como servicio adicional. Se conservan 33 pruebas Python y 3 JavaScript aprobadas y compilación Vite correcta, registradas en la iteración técnica.

## Pendientes que requieren al autor

- Institución y docente: el autor los facilitará después.
- Resultados de pruebas con compañeros: pendientes de datos reales. No se inventan participantes, observaciones ni valoraciones.
- Jade: activada y comprobada con dos respuestas reales el 19 de noviembre. Puede cometer errores conceptuales: revisar explicaciones. Evidencia en Verificacion-Jade.md.
- Voz y audio: comprobar micrófono y audición en el equipo de presentación.
- Confirmar que el profesor puede acceder al repositorio y ensayar el guion de cinco minutos.

## Preparación de la sustentación

Abrir la app con antelación. Si muestra inactividad, usar el botón para despertarla; no basta con recargar repetidamente. Abrir Wokwi y pulsar ▶, después Conectar en Guarida. Esperar ambos mensajes: broker conectado y Wokwi en línea. Mantener el simulador visible; si funciona lentamente, mantener el botón pulsado aproximadamente un segundo para que el antirrebote alcance a reconocerlo.

Mostrar la orden Ocio y su confirmación, luego el cambio desde el botón verde, iniciar una sesión y enseñar los mensajes descargables. La preparación detallada está en `DEMO_MQTT.md` y `VALIDACION_Y_SUSTENTACION.md`.

Blender, importación de otros modelos y su investigación quedan para después. Pagos y simulación de pagos permanecen fuera del alcance. Este cierre técnico no equivale a certificar todos los criterios académicos ni a sustituir los datos pendientes del autor.

## JadeUI de cierre

Se eliminó el horizonte del modelo y la barra lateral. Fondo oscuro, título hero ampliado, navegación superior, tarjeta derecha y botones flotantes con iconos vectoriales. No se incorporaron PNG no suministrados ni modelos Blender. La conexión sigue disponible en el desplegable superior.
