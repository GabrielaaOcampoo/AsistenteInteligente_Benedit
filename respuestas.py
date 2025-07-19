# -------------------------------------------------------
# Módulo: respuestas.py
# CHTBOT Benedit asistente emocional
# Función: Gestiona las respuestas que da Benedit según el intent detectado
# -------------------------------------------------------

import json          # Para cargar el archivo de intents en formato JSON
import random        # Para seleccionar aleatoriamente una respuesta
import time          # Para pausar la ejecución en momentos específicos
import webbrowser    # Para abrir videos en el navegador


# Clase principal para gestionar las respuestas del chatbot
class GestorRespuestas:
    def __init__(self, voz, intents_path):
        self.voz = voz                              # Motor de voz pasado desde main.py
        self.intents = self.cargar_intents(intents_path)  # Carga el archivo intents.json


    # Función que carga el archivo intents.json desde una ruta dada
    def cargar_intents(self, ruta):
        with open(ruta, encoding='utf-8') as f:
            return json.load(f)  # Carga el JSON como diccionario


    # Función que da una respuesta general basada en el tag detectado
    def responder(self, tag, nombre):
        for intent in self.intents["intents"]:       # Recorre todos los intents
            if intent["tag"] == tag:                 # Compara si el tag coincide
                # Elige aleatoriamente una respuesta del intent
                respuesta = random.choice(intent["responses"]).replace("{nombre}", nombre)

                # Habla la respuesta en voz alta
                self.voz.hablar(respuesta)

                # Si el intent tiene asociados múltiples videos
                if "videos" in intent:
                    video_elegido = random.choice(intent["videos"])  # Elige uno aleatoriamente
                    url = video_elegido["url"]
                    titulo = video_elegido.get("title", "Guía para calmar la mente")

                    time.sleep(15)  # Pausa para que el usuario procese la respuesta inicial
                    self.voz.hablar(f"A continuación te mostraré un video que te ayudará titulado: {titulo}")
                    webbrowser.open(url)  # Abre el video en el navegador
                    time.sleep(60)  # Espera a que el video cargue
                    self.voz.hablar(
                        "Me interesa saber cómo te sentiste con este vídeo. 💬 "
                        "¿Te hizo sentir un poco mejor o prefieres que sigamos conversando un rato más? "
                        "Recuerda que Benedit está para ti"
                    )
                    print("1. Sí, me ayudó 😊")
                    print("2. Me gustaría seguir hablando contigo 🗣️")
                    print("3. No estoy muy seguro/a todavía 🤔")

                return respuesta

        # Si no se encuentra un intent coincidente
        mensaje_error = "Disculpa, no tengo una respuesta para eso."
        self.voz.hablar(mensaje_error)
        return mensaje_error


    # Esta función responde de forma personalizada según la opción elegida por el estudiante tras ver un vídeo.
    def responder_menu_post_video(self, opcion, nombre):
        # Comprobamos qué opción eligió el usuario y generamos un mensaje adecuado para esa respuesta.

        if opcion == "1":
            # Opción 1: El video le ayudó a sentirse mejor
            mensaje = (
                f"💛 Me alegra mucho saber que el video te ayudó, {nombre}. A veces, solo necesitamos un pequeño empujón para sentirnos mejor. 🌟Recuerda que puedes volver a hablar conmigo cuando lo desees, recuerda que siempre puedes contar conmigo. Como te dije en un inicio, formas parte de mi pequeñita memoria digital jeje"
            )

        elif opcion == "2":
            # Opción 2: Quiere seguir conversando
            mensaje = (
                f"Claro, {nombre}, aquí sigo contigo. Cuéntame más sobre lo que estás sintiendo o pensando. Estoy para escucharte, tu amigo Benedit te escucha 🗣️"
            )

        elif opcion == "3":
            # Opción 3: No está seguro/a de cómo se siente
            mensaje = (
                f"Es completamente normal sentirse así, {nombre}. A veces no tenemos claro cómo nos sentimos, y eso también está bien. Puedes hablar con alguien de confianza, hacer algo que disfrutes o simplemente darte un momento. Lo que sientes es válido y merece ser escuchado. 💛"
            )

        else:
            # Opción no válida: mensaje genérico de error
            mensaje = f"No entendí esa opción, {nombre}. Por favor, elige 1, 2 o 3."

        # Usamos la clase Voz para que Benedit diga el mensaje en voz alta
        self.voz.hablar(mensaje)

        # Devolvemos el mensaje generado por si se necesita usar más adelante
        return mensaje
