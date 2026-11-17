# Activar Jade en JadeUI

Guarida es el proyecto y el cubículo; **Jade** es su asistente y **JadeUI** el nombre de la interfaz. Actualizado el 17 de noviembre de 2026.

El modelo anterior Llama 3.3 fue retirado para cuentas gratuitas y de desarrollador. El adaptador ahora usa `openai/gpt-oss-120b`, recomendado por Groq como reemplazo: https://console.groq.com/docs/deprecations . Solo muestra la respuesta final del modelo.

## Activación en la app publicada

Abre Manage app → Settings → Secrets en Streamlit. Añade `GROQ_API_KEY` con tu clave propia y guarda, conservando los demás secretos existentes. No pegues la clave en el chat, capturas, código ni repositorio. Si ya tienes `GROQ_MODEL` configurado con el modelo retirado, cámbialo a `openai/gpt-oss-120b`.

```toml
GROQ_API_KEY = "TU_CLAVE_PRIVADA"
GROQ_MODEL = "openai/gpt-oss-120b"
```

No se contratan planes ni se habilitan gastos automáticamente. La disponibilidad y límites dependen de tu cuenta. Tener una clave configurada habilita el formulario, pero solo una respuesta real verifica la conexión.

## Prueba de aceptación

1. Abrir Jade en el panel y enviar «¿Cómo te llamas y cómo puedes ayudarme a estudiar MQTT?»; comprobar identidad y respuesta en español.
2. Preparar el objetivo «Explicar publicación, suscripción y confirmación MQTT» y pedir tres pasos y una pregunta de práctica; comprobar que usa ese objetivo.
3. Pedir «Enciende las luces»; debe orientar a los controles sin afirmar que ejecutó una acción.
4. Registrar fecha y resultado sin incluir la clave. Las pruebas automatizadas usan respuestas simuladas y no sustituyen estos pasos.

Recomendación para esta versión: Groq. El adaptador ya está preparado y utiliza la biblioteca estándar de Python, por lo que no agrega dependencias de otras apps del portafolio. No se han hecho llamadas reales: falta una clave propia.

1. Crear una cuenta en https://console.groq.com y generar una clave desde API Keys. Consultar las cuotas y condiciones de la cuenta; no activar gastos para esta prueba sin decidirlo previamente.
2. Copiar `.streamlit/secrets.toml.example` como `.streamlit/secrets.toml` y colocar la clave entre las comillas. No pegarla en una conversación ni subir ese archivo al repositorio.
3. Reiniciar Streamlit. En Estudio aparecerá el formulario “Habla con Jade”.
4. Preparar un objetivo y enviar: “Ayúdame a dividir este objetivo en tres tareas concretas y una pregunta de autoevaluación”.
5. Revisar que la respuesta corresponda al objetivo, editar las tareas manualmente y comprobar que el asistente no afirme haber cambiado el cubículo.

En Streamlit Community Cloud, colocar `GROQ_API_KEY` en la configuración Secrets de la app. También se admite la variable de entorno del mismo nombre. El modelo predeterminado es `openai/gpt-oss-120b`; puede cambiarse con la variable `GROQ_MODEL` si la cuenta requiere otro modelo compatible.

La app envía el objetivo y hasta doce mensajes recientes cuando se pulsa Enviar. No hay envío automático de audio ni datos por MQTT. La lista inicial de tareas sigue siendo una guía por reglas. Si falta la clave o falla el servicio, esa guía continúa disponible.

Alternativa para evaluar después: Gemini API. También requiere cuenta y credencial propias, y tiene condiciones/cuotas por modelo. No se implementaron dos proveedores a la vez: mantener un adaptador pequeño reduce cambios y facilita depurar la entrega.

Fuentes: [inicio de Groq](https://console.groq.com/docs/quickstart), [límites](https://console.groq.com/docs/rate-limits), [precios y condiciones de Gemini](https://ai.google.dev/gemini-api/docs/pricing).
