# Demostración de Guarida y Wokwi

## Preparación

Abre https://guaridastudio.streamlit.app/ y https://wokwi.com/projects/480507284209602561 en dos ventanas visibles. Usa en ambos el código `jhuza-guarida-20261108`. No ejecutes dos simuladores con el mismo código durante la demostración.

En Streamlit pulsa **Conectar**. El aviso **Broker MQTT conectado** acredita la conexión de la app al servidor, pero todavía no la del ESP32. En Wokwi pulsa ▶; espera WiFi y MQTT. La app mostrará **Wokwi en línea** cuando reciba un mensaje reciente.

Por defecto la app usa WebSocket seguro en 8884; Wokwi usa TCP en 1883 hacia el mismo broker HiveMQ. Son dos transportes del mismo protocolo MQTT y comparten los mismos canales. TCP 1883 queda disponible como alternativa en la app si falla el primero.

## Cuatro estados coherentes

| Panel | Estado MQTT | Botón Wokwi | GPIO |
|---|---|---|---|
| Bienvenida | disponible | Amarillo | 27 |
| Estudio | concentracion | Azul | 25 |
| Ocio | gamer | Morado | 33 |
| Descanso | descanso | Verde | 26 |

El naranja y el rojo son avisos visuales de transición y tiempo restante, no ambientes adicionales ni botones independientes.

## Ensayo frente al profesor

1. Desde el panel Ambiente elige Estudio y después Ocio. Comprueba el estado en la OLED y en el monitor serie de Wokwi.
2. Abre **Evidencia de mensajes** en Streamlit. Una respuesta con `source: wokwi`, `cause: command` y el identificador de la orden muestra la confirmación de Wokwi.
3. Pulsa Descanso en el circuito. Comprueba que la app cambia a Descanso y recibe `cause: button`. Esto demuestra el sentido Wokwi → app, independiente de una orden de la interfaz.
4. En Sesión selecciona Estudio u Ocio y comienza un bloque. El contador debe arrancar después de la confirmación coincidente, no al enviar la orden.
5. Detén Wokwi. Tras unos 15 segundos sin mensajes, la app debe indicar falta de señal aunque el broker siga conectado. Reinicia y comprueba recuperación.
6. Descarga los mensajes para conservar evidencia de la prueba.

## Si no conecta

- Sin conexión al broker: prueba el otro transporte y pulsa Conectar; consulta el aviso de error junto al botón.
- Broker conectado, sin Wokwi: inicia la simulación, revisa el código de cubículo y comprueba WiFi/MQTT en Wokwi.
- Solo tres botones o el estado gamer no responde: copia los archivos `wokwi/sketch.ino` y `wokwi/diagram.json` de esta versión al proyecto y guárdalos con la cuenta propietaria.
- El navegador puede ralentizar una simulación en segundo plano. Mantén ambas ventanas visibles durante la prueba; el aviso de señal reciente mide tiempo real.

El broker público sirve para este prototipo: solo se publican estados técnicos. No transmite objetivos, conversaciones de IA ni archivos de audio. Blender y nuevos modelos quedan fuera de esta entrega de conectividad.
