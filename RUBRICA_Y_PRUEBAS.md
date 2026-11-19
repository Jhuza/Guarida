# Guarida · verificación de rúbrica

Revisión técnica: 19 de noviembre de 2026. Matriz basada en los criterios y pesos previamente registrados en el proyecto. No asigna calificación ni sustituye la evaluación del docente. Historial detallado: HISTORIAL_PRUEBAS.md.

| Criterio | Evidencia verificable | Estado y límite |
|---|---|---|
| A1 · Wokwi · 10 % | ESP32, OLED y cuatro botones; proyecto original guardado y compilado. | Verificado en prueba real previa. |
| A2 · MQTT bidireccional · 10 % | App→Wokwi, botón→app, confirmaciones por id, detección de desconexión. Evidencia pública del 16 de noviembre en CIERRE_ENTREGA.md. | Verificado; depende de internet y broker público. |
| A3 · Dos ambientes · 8 % | Páginas Estudio y Descanso; zonas escritorio y sofá en Babylon. | Implementado; interpretación académica corresponde al docente. |
| A4 · Modalidades · 10 % | Texto, botones, 3D, voz, síntesis, archivo de música y Jade real. | Jade verificada el 19; audición y reconocimiento humano pendientes. |
| A5 · Código · 7 % | Python modular, React/Vite/Babylon, firmware, dependencias fijadas, 33 pruebas Python y 3 JavaScript aprobadas. | Código preparado; confirmar acceso del evaluador al repositorio privado. |
| B1 · Usabilidad · 8 % | Etiquetas además de color, alternativas por botones, estados de error y navegación superior. | Revisión técnica realizada; sin evaluación con participantes. |
| B2 · Innovación · 7 % | Entorno 3D, estados IoT y organización de estudio; fundamentos en el informe. | Propuesta documentada, sin eficacia demostrada. |
| C1 · Demo · 8 % | Guion y evidencias de MQTT y Jade disponibles. | Ensayo presencial con red de clase a cargo del autor. |
| C2 · Dominio · 8 % | Arquitectura, protocolo y preguntas de sustentación documentados. | Competencia oral del estudiante, no certificable por software. |
| C3 · Tiempo y claridad · 4 % | Guion de cinco minutos. | Cronometrar presentación del autor. |
| D · Informe · 20 % | Diez apartados, referencias, resultados y límites explícitos. | Faltan institución y docente; no se inventaron participantes. |

## Comprobaciones del 19 de noviembre

- 33 pruebas Python aprobadas; 3 pruebas JavaScript aprobadas; compilación Vite correcta.
- Jade respondió en la app pública, conservó el contexto y aclaró que no controla hardware desde el chat. Una respuesta inicial confundió QoS; se corrigió al señalarlo. Se informa al usuario que debe verificar las explicaciones.
- Vista local: fondo oscuro sin plano exterior ni horizonte; navegación Ambiente/Jade/Sesión; páginas Estudio/Descanso arriba; puerta, recorrido, privacidad y cambio de ambiente operativos.
- No se afirma una tasa de fotogramas ni mejora porcentual de carga. Se conserva la carga diferida de Babylon, pausa en pestaña oculta y matrices estáticas; se eliminó la malla de entorno que causaba el horizonte.
- PNG personalizados no recibidos: los controles usan iconos vectoriales accesibles con estados de selección y hover.

## Alcance excluido

Pagos, cuentas, hardware físico y modelos de Blender no forman parte de esta entrega. La conversación no se persiste en una base de datos. La clave permanece en Streamlit Secrets, fuera del código y el paquete.
