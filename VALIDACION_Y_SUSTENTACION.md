# Guarida: cierre de validación y sustentación

## Prueba breve con participantes (pendiente de realizar)

Invitar inicialmente a tres compañeros de forma voluntaria. Es una evaluación exploratoria, no una muestra representativa. Identificarlos P01, P02 y P03; no registrar datos personales ni grabar sin permiso. Explicar: “Estamos probando la aplicación, no tus capacidades”. Registrar lo que ocurra, incluso fallos; no completar resultados de antemano.

| Tarea | Consigna neutral | Comprobación |
|---|---|---|
| T1 | Prepara una sesión para una tarea tuya. | Define objetivo y entiende las tareas. |
| T2 | Cambia una tarea y marca otra como terminada. | Encuentra edición y comprende progreso. |
| T3 | Comienza un bloque de estudio. | Distingue solicitud y confirmación; inicia contador. |
| T4 | Cambia a descanso desde Wokwi. | Reconoce el cambio en app y 3D. |
| T5 | Pide descanso por voz y escucha la bienvenida. | Permiso, reconocimiento y audición; anotar navegador. |
| T6 | Activa y detén el sonido a volumen cómodo. | Audio audible y control comprensible. |
| T7 | Con Wokwi detenido, explica lo que ves. | Comprende pérdida de señal y no confunde estado anterior con actual. |

Registrar por tarea: participante, fecha, navegador/dispositivo, éxito sin ayuda / con ayuda / fallo, tiempo aproximado, error observado y comentario literal opcional. Preguntar al final: “¿Qué fue confuso?”, “¿Qué cambiarías primero?” y facilidad de uso de 1 a 5. No interpretar esa escala como SUS ni como medida de aprendizaje.

Tras cada sesión: priorizar problemas que impiden completar tareas, hacer correcciones y repetir únicamente los casos afectados. Añadir resultados agregados y limitaciones al apartado 8 del informe. No registrar “aprobado” si no se ejecutó la tarea.

## Guion de cinco minutos (duración propuesta)

| Tiempo | Qué mostrar y explicar |
|---|---|
| 0:00–0:40 | Problema y protopersona provisional; ausencia de entrevistas. |
| 0:40–1:15 | Circuito virtual: ESP32, OLED, tres botones. Arquitectura y dos temas MQTT. |
| 1:15–2:05 | Objetivo, edición de tareas, iniciar concentración y esperar confirmación. |
| 2:05–2:45 | Botón Descanso en Wokwi; observar Streamlit y Babylon. Navegar a Descanso. |
| 2:45–3:25 | Voz y audio si fueron probados en ese navegador. Alternativa por botones. |
| 3:25–4:00 | Detener Wokwi y esperar el indicador de falta de señal. |
| 4:00–4:35 | Pruebas, informe, código y limitaciones. IA solo si ya se activó y probó; de lo contrario mostrar estado pendiente. |
| 4:35–5:00 | Aporte, trabajo futuro y cierre. |

Hacer un ensayo cronometrado antes de clase; ajustar al tiempo que indique el profesor. Confirmar internet, acceso al broker, WSS/CDN, permisos de micrófono, volumen y coincidencia del código de sala. Las capturas son respaldo explicativo y no sustituyen una demo en vivo.

## Preguntas técnicas para practicar

- **¿Por qué MQTT?** Permite que Wokwi, Streamlit y la vista reciban cambios sin conectarse directamente entre sí.
- **¿Cómo demuestras bidireccionalidad?** Una orden de Streamlit cambia el firmware y vuelve con el mismo id; un botón de Wokwi produce un cambio independiente recibido por la app.
- **¿Enviar es confirmar?** No. La confirmación la emite el dispositivo con id y estado coincidentes.
- **¿Qué ocurre si falla internet?** Se informa la falta de conexión o señal; la organización local de tareas sigue disponible. El control remoto necesita conexión.
- **¿Por qué WSS en Babylon?** MQTT.js en el navegador usa WebSockets; Python y ESP32 pueden usar TCP.
- **¿Qué hace Babylon?** Representa el espacio y el estado; no reemplaza el circuito ni demuestra por sí solo una comunicación con Wokwi.
- **¿Qué parte es IA?** Únicamente el chat opcional con Groq. La lista inicial se genera por reglas; las respuestas del adaptador se probaron con simulaciones, aún sin clave real.
- **¿Cómo proteges datos?** Objetivos/chat no se publican en MQTT. El chat sí se envía a Groq al pulsar Enviar; la clave está en el servidor. El broker público solo sirve para una demostración.
- **¿La música mejora la concentración?** No se ha demostrado en este proyecto. Son tonos estéreo opcionales y una preferencia de la protopersona.
- **¿Qué falta para un producto real?** Validar con usuarios, autenticar comunicaciones, desplegar y probar recuperación/durabilidad; las funciones físicas futuras requieren diseño adicional.

## Evidencias que todavía deben obtenerse

- URL guardada de Wokwi y URL del repositorio publicado.
- URL de Streamlit si la entrega exige acceso remoto; prueba desde otra sesión/navegador.
- Prueba real del chat con una clave propia, si se presenta como funcionalidad activa.
- Pruebas de voz y audición con una persona y evaluación de usabilidad.
- Ensayo cronometrado y revisión final del informe con los datos de institución/docente.

Estos puntos no se convierten en resultados por tener este documento: deben ejecutarse y registrarse.
