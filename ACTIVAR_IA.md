# Activar el asistente de Guarida

Recomendación para esta versión: Groq. El adaptador ya está preparado y utiliza la biblioteca estándar de Python, por lo que no agrega dependencias de otras apps del portafolio. No se han hecho llamadas reales: falta una clave propia.

1. Crear una cuenta en https://console.groq.com y generar una clave desde API Keys. Consultar las cuotas y condiciones de la cuenta; no activar gastos para esta prueba sin decidirlo previamente.
2. Copiar `.streamlit/secrets.toml.example` como `.streamlit/secrets.toml` y colocar la clave entre las comillas. No pegarla en una conversación ni subir ese archivo al repositorio.
3. Reiniciar Streamlit. En Estudio aparecerá el formulario “Habla con Guarida”.
4. Preparar un objetivo y enviar: “Ayúdame a dividir este objetivo en tres tareas concretas y una pregunta de autoevaluación”.
5. Revisar que la respuesta corresponda al objetivo, editar las tareas manualmente y comprobar que el asistente no afirme haber cambiado el cubículo.

En Streamlit Community Cloud, colocar `GROQ_API_KEY` en la configuración Secrets de la app. También se admite la variable de entorno del mismo nombre. El modelo predeterminado es `llama-3.3-70b-versatile`; puede cambiarse con la variable `GROQ_MODEL` si la cuenta requiere otro modelo compatible.

La app envía el objetivo y hasta doce mensajes recientes cuando se pulsa Enviar. No hay envío automático de audio ni datos por MQTT. La lista inicial de tareas sigue siendo una guía por reglas. Si falta la clave o falla el servicio, esa guía continúa disponible.

Alternativa para evaluar después: Gemini API. También requiere cuenta y credencial propias, y tiene condiciones/cuotas por modelo. No se implementaron dos proveedores a la vez: mantener un adaptador pequeño reduce cambios y facilita depurar la entrega.

Fuentes: [inicio de Groq](https://console.groq.com/docs/quickstart), [límites](https://console.groq.com/docs/rate-limits), [precios y condiciones de Gemini](https://ai.google.dev/gemini-api/docs/pricing).
