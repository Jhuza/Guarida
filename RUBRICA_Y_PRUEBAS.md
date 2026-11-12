# Guarida · seguimiento de la rúbrica

Actualizado: 9 de noviembre de 2026. Esta matriz registra evidencias; no asigna una nota ni afirma que la entrega esté completa.

Actualización de entrega, 12 de noviembre de 2026: código, pruebas, circuito, informe y capturas subidos a [Jhuza/Guarida](https://github.com/Jhuza/Guarida), repositorio privado. La publicación pendiente de A5 queda realizada; todavía falta comprobar acceso del evaluador e instalación en destino. Esta actualización no implica nuevas pruebas funcionales.

| Criterio | Evidencia actual | Trabajo pendiente |
|---|---|---|
| A1 · Wokwi, 10 % | Circuito ESP32, pantalla OLED y tres botones; firmware compiló y publicó estados en la sesión anterior. | Guardar proyecto en cuenta; la ida y vuelta se verificó el 9 de noviembre. |
| A2 · Bidireccional, 10 % | Publicación y recepción MQTT, identificadores de orden y confirmación. Cinco pruebas de red reales con emulador Python aprobadas. | Ida y vuelta real comprobada el 9 de noviembre; conservar evidencia. |
| A3 · Dos ambientes, 8 % | Páginas Estudio y Descanso, ambas abiertas en navegador, con zonas distintas en la escena. | Validar con el profesor su interpretación de dos ambientes. |
| A4 · Modalidades, 10 % | Texto, botones, escena manipulable, comandos de voz, síntesis, tono estéreo y adaptador de chat opcional implementados. | Probar micrófono/audio con una persona y chat con una clave real. |
| A5 · Código/repositorio, 7 % | Módulos separados, versiones fijadas, 17 pruebas aprobadas, dependencias compatibles y repositorio Git local inicializado. | Publicar repositorio y comprobar instalación desde cero en destino. |
| B1 · Usabilidad, 8 % | Texto de estado además del color; alternativa por botones y mensajes de error. | Pruebas reales con compañeros y correcciones registradas. |
| B2 · Innovación, 7 % | Relación entre organización de sesión, disponibilidad y espacio 3D. | Sustentar la pertinencia con investigación, no con beneficios supuestos. |
| C1 · Demo, 8 % | Recorrido y condiciones de ensayo en VALIDACION_Y_SUSTENTACION.md. | Ensayo completo con Wokwi activo y conexión de clase. |
| C2 · Dominio, 8 % | Arquitectura, protocolo y diez preguntas técnicas preparados. | Explicación y práctica por parte del estudiante. |
| C3 · Claridad/tiempo, 4 % | Guion distribuido en cinco minutos. | Cronometrar y ajustar a lo indicado por el profesor. |
| D · Informe, 20 % | INFORME_GUARIDA.md contiene los diez apartados exigidos. | Completar institución/docente, enlaces de publicación y resultados con participantes cuando existan; revisión final del autor. |

## Pruebas realizadas

- 17 pruebas automatizadas aprobadas: protocolo, temporizador, objetivo vacío, tareas, uso sin conexión, edición, arranque solo tras confirmación, cancelación de arranque pendiente y respuesta/errores del adaptador IA con servicio simulado. Registro: pruebas-automatizadas.txt. `pip check` no detectó dependencias incompatibles.
- 5 comprobaciones de red aprobadas el 8 de noviembre: los tres estados por TCP, evento independiente del dispositivo y comunicación WebSockets seguros ↔ TCP. Dispositivo utilizado: emulador Python explícito, no Wokwi.
- Inspección visual: escena Babylon renderizada; navegación entre páginas Estudio y Descanso; creación de lista desde un objetivo.
- Wokwi: compilación y mensajes de arranque/heartbeat observados el 8 de noviembre. Al reabrir el 9, hubo un error temporal `Failed to fetch` del servicio de compilación y se reintentó.

No se han validado todavía la calidad del reconocimiento de voz, audición del sonido, conexión real con IA ni despliegue en Streamlit Cloud. No hay entrevistas ni encuestas realizadas. La revisión actual en navegador comprobó edición de tareas, navegación y conservación del progreso entre páginas; captura evidencia-tareas-ia.png.

## Guion de demostración

1. Explicar que la protopersona es provisional y el objetivo es ayudar a estructurar el estudio.
2. Mostrar circuito Wokwi ejecutándose y conectar Guarida.
3. Escribir un objetivo y mostrar las tareas, aclarando que en esta versión se generan por reglas.
4. Solicitar concentración y señalar el identificador y la confirmación del dispositivo.
5. Pulsar Descanso en Wokwi y mostrar el cambio en Streamlit y la escena.
6. Abrir página Descanso y demostrar el temporizador.
7. Detener Wokwi y mostrar pérdida de señal, sin presentar datos antiguos como actuales.

## Apartados redactados del informe

1. Portada y resumen.
2. Introducción, problema y objetivos (hipótesis explícita).
3. Marco teórico con fuentes sobre interacción multimodal, organización del estudio e IoT.
4. Requerimientos y casos de uso.
5. Arquitectura: Streamlit, broker, Wokwi y Babylon.
6. Hardware simulado: cableado, pantalla, entradas y firmware.
7. Aplicación Streamlit: páginas, estados y modalidades.
8. Pruebas y resultados, distinguiendo automatización de evaluación con usuarios.
9. Conclusiones y trabajo futuro: activar IA, validación y despliegue; hardware físico fuera del alcance.
10. Referencias y anexos: código, capturas, mensajes y guion.

## Evidencia de integración real · 9 de noviembre

Streamlit envió concentración con id cea5778c11d742e2aa43dd16ae0cf1f6. Wokwi devolvió el mismo id con source=wokwi y cause=command. La app indicó Confirmado y la escena mostró concentración. Después, el botón amarillo de Wokwi publicó descanso con cause=button; ambos clientes mostraron Descanso. Captura: evidencia-descanso.png. El fallo temporal de compilación se resolvió al reintentar.


También se detuvo Wokwi: Streamlit y Babylon mostraron Sin señal reciente. Captura: evidencia-desconexion.png. El control de sonido cambió entre Sonido y Silenciar; esto valida la interacción, no la audición ni la eficacia del audio.
