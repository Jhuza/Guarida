# Guarida · simulación de estudio

Prototipo académico de Juan José Hoyos. Streamlit + MQTT + ESP32 virtual en Wokwi + Babylon.js. Sin hardware físico.

Repositorio: [Jhuza/Guarida](https://github.com/Jhuza/Guarida). Subido el 12 de noviembre de 2026 como privado. Para que el profesor pueda revisarlo, será necesario darle acceso o decidir su publicación pública antes de entregar.

## Ejecutar

Python 3.14 fue el entorno probado. Desde esta carpeta:

```powershell
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
.venv/Scripts/python -m streamlit run app.py
```

En este computador ya existe el entorno `../../work/venv`.

## Wokwi

1. Abrir https://wokwi.com/projects/new/esp32.
2. Copiar `wokwi/sketch.ino` y `wokwi/diagram.json` en las pestañas correspondientes.
3. Añadir las bibliotecas de `wokwi/libraries.txt` en Library Manager, o pegar ese archivo en la pestaña libraries.txt.
4. Iniciar simulación y esperar conexión Wi-Fi y MQTT.
5. En Streamlit, pulsar Conectar. El código de cubículo debe coincidir con ROOM del firmware.

La sesión de Wokwi no está guardada en una cuenta: conservar estos archivos y guardar una copia del proyecto al iniciar sesión.

## Arquitectura

Streamlit publica órdenes JSON en `guarida/{room}/command`; Wokwi las valida, cambia su pantalla y publica confirmación en `guarida/{room}/state`. Los botones físicos simulados producen eventos independientes. La escena Babylon recibe el mismo estado por MQTT sobre WebSockets seguros y permite enviar órdenes.

Cada solicitud tiene un identificador. Publicar no equivale a confirmar. Se muestran solicitudes pendientes y pérdidas de señal. El broker público solo transporta estados técnicos; no recibe objetivos, conversaciones ni audio. Es una infraestructura de demostración sin autenticación, no un servicio de producción.

Estudio y Descanso son páginas distintas, con dos zonas visibles en 3D. Los controles de voz dependen del navegador; los botones permanecen como alternativa. El audio actual es una demostración de tonos estéreo, no una playlist musical ni un tratamiento.

## Alcance real

La lista inicial de tareas es una guía por reglas, editable. El chat opcional con Groq está implementado, pendiente de activar con una clave propia y verificar con el servicio real: ver [ACTIVAR_IA.md](ACTIVAR_IA.md). No agrega un SDK ni mezcla bibliotecas del portafolio. La conversación de audio con IA y la bienvenida flotante completa siguen pendientes. No se han realizado entrevistas, encuestas ni pruebas con estudiantes. No se atribuyen mejoras demostradas de concentración.

El temporizador iniciado desde Streamlit espera una confirmación del estado solicitado. Los cambios iniciados desde Wokwi o la escena cambian la disponibilidad, pero no arrancan automáticamente el contador. La organización de tareas y el chat se conservan en la sesión, no en una base de datos; descargar el resumen antes de cerrarla.

## Material para entregar

- [Informe con los diez apartados](INFORME_GUARIDA.md).
- [Matriz de rúbrica y evidencias](RUBRICA_Y_PRUEBAS.md).
- [Prueba con participantes y guion de sustentación](VALIDACION_Y_SUSTENTACION.md).

Antes de entregar, guardar el proyecto en una cuenta de Wokwi y añadir su enlace; comprobar también el acceso del profesor al repositorio. La publicación en Streamlit requiere seleccionar `app.py` como archivo de entrada, instalar `requirements.txt` y configurar secretos si se activa la IA. El despliegue aún no está comprobado; verificar conectividad MQTT desde el servidor de destino.

## Pruebas

```powershell
python -m unittest discover -s tests -v
$env:PYTHONPATH='.'
python tests/network_probe.py
```

`network_probe.py` usa un emulador Python identificado como tal y un canal aleatorio. No sustituye las pruebas del circuito Wokwi.

## Fuentes técnicas consultadas

- https://docs.wokwi.com/guides/esp32-wifi — red virtual y MQTT.
- https://docs.wokwi.com/parts/board-ssd1306 — pantalla I2C vigente, dirección 0x3c.
- https://docs.wokwi.com/parts/wokwi-pushbutton — contactos y resistencias pull-up.
- https://docs.streamlit.io/develop/api-reference/execution-flow/st.fragment — actualización parcial del estado y temporizador.
- https://github.com/mqttjs/MQTT.js#browser — MQTT en navegador requiere WebSockets.
- https://doc.babylonjs.com/features/ — motor 3D de navegador.

Se reemplazó el componente HTML antiguo de Streamlit por st.iframe, comprobando su API instalada. Se fijaron las versiones de dependencias para evitar combinar requisitos incompatibles del portafolio.
