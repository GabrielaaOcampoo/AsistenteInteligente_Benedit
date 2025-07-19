# CHATBOT Benedit, tu asistente emocional universitario 😊
# Este fragmento de código me permite hablar contigo usando voz,
# haciendo nuestra conversación más cercana y humana.

# Importa la librería pyttsx3 para convertir texto en voz
import pyttsx3

# Importa la librería time para poder hacer pausas durante la ejecución
import time

# Importa la librería re para trabajar con expresiones regulares (útil para limpiar el texto)
import re

# Definición de la clase Voz, que permite a Benedit hablar con el usuario
class Voz:
    # Método para hablar en voz alta un mensaje de texto
    def hablar(self, mensaje):
        print("Benedit:", mensaje)  # Muestra el mensaje en pantalla

        # Elimina emojis y caracteres especiales que el motor de voz no puede pronunciar
        mensaje_para_voz = re.sub(r'[^\w\s,.!?¿¡]', '', mensaje)

        # Inicializa el motor de texto a voz
        engine = pyttsx3.init()

        # Indica al motor qué mensaje debe decir
        engine.say(mensaje_para_voz)

        # Ejecuta la reproducción de voz
        engine.runAndWait()

        # Espera medio segundo antes de continuar con el siguiente proceso
        time.sleep(0.5)
