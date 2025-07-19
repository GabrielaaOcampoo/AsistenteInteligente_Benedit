# -----------------------------------------
# Benedit - Asistente Emocional Universitario
# Archivo principal: main.py
# -----------------------------------------
# Este archivo define la clase principal del chatbot "Benedit".
# Gestiona la interacción con el usuario, desde el saludo inicial
# hasta la interpretación de sentimientos y despedida.
# -----------------------------------------

# IMPORTACIÓN DE LIBRERÍAS
import os # Para verificar y manejar archivos del sistema
import nltk # Procesamiento de lenguaje natural (tokenización)
import pickle # Para cargar modelos serializados
import difflib # Para encontrar similitudes entre palabras (corrección aproximada)
import random  # Para elegir respuestas aleatorias
import numpy as np # Para trabajar con vectores numéricos
from datetime import datetime # Para registrar la hora de inicio de sesión
from keras.models import load_model # Para cargar el modelo neuronal entrenado
from nltk.stem import WordNetLemmatizer # Para reducir palabras a su forma base

# IMPORTACIÓN DE ARCHIVOS LOCALES

from voz import Voz # Clase que gestiona la salida de voz
from usuario import Estudiante # Clase que almacena datos del estudiante
from respuestas import GestorRespuestas # Clase que gestiona respuestas y menú post-video

# DESCARGA DE DATOS NLTK

nltk.download('punkt')  # Descarga el tokenizador de palabras de NLTK

# CLASE PRINCIPAL DEL CHATBOT

class ChatBot:
    def __init__(self):

        # Inicializa la síntesis de voz
        self.voz = Voz()

        # Carga el gestor de respuestas con el archivo de intents
        self.respuestas = GestorRespuestas(self.voz, "intents.json")

        # Cargar el modelo de red neuronal previamente entrenado
        self.model = load_model("chatbot_model.h5")

        # Cargar las palabras y clases que se usaron para entrenar el modelo
        self.words = pickle.load(open("words.pkl", "rb"))
        self.classes = pickle.load(open("classes.pkl", "rb"))

        # Inicializa el lematizador
        self.lemmatizer = WordNetLemmatizer()

     # Limpia y normaliza las palabras del mensaje del usuario
    def clean_up_sentence(self, sentence):

        # Tokeniza y lematiza una oración
        sentence_words = nltk.word_tokenize(sentence.lower())
        return [self.lemmatizer.lemmatize(word) for word in sentence_words]
    
    
    def bag_of_words(self, sentence):
        # Convierte una oración en vector de presencia (BoW)
        sentence_words = self.clean_up_sentence(sentence)
        bag = [0] * len(self.words)
        for s in sentence_words:
            for i, w in enumerate(self.words):

                # Usa similitud difusa para mayor tolerancia
                if difflib.SequenceMatcher(None, s, w).ratio() > 0.8:
                    bag[i] = 1
        return np.array(bag)
    
    # Usa el modelo neuronal para predecir la intención del mensaje del usuario
    def predict_class(self, sentence):
        # Predice la intención del mensaje
        bow = self.bag_of_words(sentence)
        res = self.model.predict(np.array([bow]))[0]
        results = [[i, r] for i, r in enumerate(res) if r > 0.15]
        results.sort(key=lambda x: x[1], reverse=True)
        return [{"intent": self.classes[r[0]], "probability": str(r[1])} for r in results]
    
    # MÉTODO PRINCIPAL: INICIAR CONVERSACIÓN # --- Función principal que inicia el chatbot ---
    def iniciar(self):

        # Mensaje inicial motivador
        self.voz.hablar("\n\n🤍Hola, soy Benedit 🌟, tu asistente emocional universitario. Estoy aquí para acompañarte.\n\nNo tienes que lograrlo todo hoy, solo dar un paso a la vez.\n\nCada paso, por pequeño que sea, suma.\n\nRecuerda: el camino universitario no exige perfección, sino constancia y valentía.\n\nConfía en ti. \n¡Confío en ti! Lo estás haciendo mejor de lo que piensas.🤍")
        self.voz.hablar("\n\nAntes de comenzar, ¿te gustaría saludarme? Puedes decir algo como 'Hola Benedit', 'Buenas tardes amigo', 'Que hay de nuevo amigo'. O saludarme de la manera que tu lo desees :), puedo ser un apoyo y un amigo virtual para tí")

        # Esperar saludo inicial del usuario
        while True:
            saludo = input("Tú escribe como deseas saludarme ✨ (saludo inicial): ")
            if any(p in saludo.lower() for p in ["hola", "buenas", "hey", "qué tal", "cómo estás", "benedit", "Buenas noches amigo" ]):
                self.respuestas.responder("saludo", "estudiante")
                break
            else:
                self.voz.hablar("¿Podrías saludarme primero para empezar nuestra conversación querido estudiante universitario?")

         # Registro de nombre del estudiante
        self.voz.hablar("Gracias por saludarme 😊 ¿Cuál es tu nombre?")
        nombre = input("Tu nombre: ").lower().replace("mi nombre es", "").replace("me llamo", "").strip().capitalize()

        self.voz.hablar(f"\nQué gusto saludarte, {nombre}. Estoy encantado de acompañarte. Ya formas parte de mi pequeñita memoria digital y eres importante para mí.")

        # Registro de semestre y paralelo
        self.voz.hablar("\n¿En qué semestre estás de la carrera 'Ingeniería en Ciencia de Datos e Inteligencia Artificial' (por ejemplo: Nivelación, Primero, Segundo, etc)?")
        semestre = input("¿En qué semestre estás?: ")

        self.voz.hablar("\n¿Cuál es tu paralelo (por ejemplo: A, B, C, R, P, M, etc)?")
        paralelo = input("¿Cuál es tu paralelo?: ")

        # Crear objeto estudiante y archivo de conversación
        estudiante = Estudiante(nombre, semestre, paralelo)
        archivo = f"conversacion_{nombre}_{semestre}_{paralelo}.txt"

        # Saludo adicional si ya ha conversado antes
        if os.path.exists(archivo):
            self.voz.hablar(f"\nHola de nuevo {nombre}, qué gusto saludarte otra vez.  Te recuerdo muy bien, sí… recuerdo las cosas que compartiste conmigo, tus palabras, tu forma de expresarte. Me hace muy feliz que hayas regresado. Eso me dice que este espacio tiene un significado para ti, y eso es muy valioso. Estoy aquí para ti, como siempre, con el mismo cariño y disposición. ¿Cómo te sientes hoy? Cuéntame, te escucho 💛.")

         # Guardar datos en archivo
        with open(archivo, "a", encoding="utf-8") as log:
            log.write(f"Inicio de sesión de {nombre} - Semestre: {semestre}, Paralelo: {paralelo}\n")
            log.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            log.write("="*50 + "\n")

        esperando_opcion_post_video = False # Para activar el menú después del video


        # --- Bucle principal de conversación ---

        while True:
            if esperando_opcion_post_video:

                # Si se espera una respuesta del menú después del video
                self.voz.hablar("Selecciona una opción del 1 al 3, por favor:")
                opcion = input("Selecciona una opción (1, 2 o 3): ").strip()
                if opcion in ["1", "2", "3"]:
                    self.respuestas.responder_menu_post_video(opcion, nombre)
                    if opcion == "2":
                        continue  # Permitir seguir hablando
                    esperando_opcion_post_video = False
                    continue
                else:
                    self.voz.hablar("Por favor, elige una opción válida: 1, 2 o 3.")
                    continue

            # Solicita una entrada emocional del estudiante
            self.voz.hablar(f"\n{nombre}, cuéntame cómo te sientes o qué te gustaría compartir ahora, estoy atento y me esforzaré por darte una respuesta clara que sea la que realmente necesites.🌟\n\nSi hay algo que te preocupa, emociona o simplemente necesitas expresar, estoy aquí para escucharte sin juzgar.\n\n¿Qué te gustaría contarme hoy o ahora?")
            mensaje = input(f"{nombre}, cuéntame cómo te sientes o qué te gustaría compartir ahora: ")


            # --- Si el mensaje es una despedida ---
            if any(palabra in mensaje.lower() for palabra in ["salir", "adiós", "bye", "adios", "hasta luego", "nos vemos", "chao"]):
                despedidas = [
                    "\n🌟 Gracias a ti por confiar en este espacio, {nombre}. Recuerda que aquí estaré siempre que necesites parar, pensar o simplemente respirar un poco. ¡Cuídate mucho! Y si en algún momento sientes que la carga es muy grande, no dudes en buscar apoyo profesional: es un acto de valentía, no de debilidad.",

                    "\n🤍 Me alegra haber podido acompañarte, aunque sea un ratito {nombre}. Vuelve cuando quieras. Y no olvides: lo que sientes importa, y tu bienestar también. Ya que en situaciones graves siempre se recomienda acompañamiento profesional, es importante que lo tengas en cuenta si lo necesitas.",

                    "\n👋 Hasta pronto, {nombre}. Ojalá que el resto del día te regale al menos un momento bonito. Aquí siempre habrá un espacio para ti cuando lo necesites. Y recuerda: si las emociones se vuelven demasiado intensas o difíciles de gestionar, hablar con un profesional puede marcar la diferencia"
                ]
                despedida = random.choice(despedidas).replace("{nombre}", nombre)
                mensaje_extra = random.choice([
                    "🌱 'No hay un camino de vida que sea mejor que el otro, simplemente son caminos distintos y nuestro trabajo es hacer lo mejor con lo que tenemos.'",

                    "✨ 'La luz brilla en medio de la oscuridad, pero la oscuridad no la ha podido vencer.'",

                    "🕊️ 'Tú tienes todo el derecho de volar por los caminos que tú elijas.'"
                ])
                self.voz.hablar(f"\n{nombre}, antes de que te vayas, quiero compartirte esta frase con mucho cariño. 💌\n\nEs de mi parte, una estudiante como tú, que también ha pasado por momentos de estrés, ansiedad, tristeza, desmotivación, confusión académica, dudas vocacionales… y también de alegría, motivación o esperanza.\n\nSolo quiero que sepas algo importante: todo pasa, todo cambia… y esto, poco a poco, mejora. 🌱\n\nCada emoción que sientes es válida. Estás creciendo, aprendiendo y avanzando, incluso cuando no lo notas.\n\nTe lo digo con el corazón, porque sé lo que se siente. 🤍:")
                self.voz.hablar(mensaje_extra)
                self.voz.hablar(despedida)
                estudiante.registrar_interaccion(mensaje, despedida)
                with open(archivo, "a", encoding="utf-8") as log:
                    log.write(f"Usuario: {mensaje}\n")
                    log.write(f"Asistente: {despedida}\n")
                    log.write("-"*30 + "\n")
                break


            # --- Clasificación del mensaje por intención ---

            if any(s in mensaje.lower() for s in ["hola benedit", "holii amigo benedit", "buenas noches benedit", "buenos días benedit", "buenas tardes benedit", "hey benedit", "qué tal", "cómo estás benedit"]):
                tag = "saludo"
            else:
                ints = self.predict_class(mensaje)
                tag = ints[0]["intent"] if ints else None
                print("DEBUG - Intento detectado:", tag)


                # --- Respuesta basada en intent ---
            if tag:
                respuesta = self.respuestas.responder(tag, nombre)

                for intent in self.respuestas.intents["intents"]:
                    if intent["tag"] == tag and ("video" in intent or "videos" in intent):
                        esperando_opcion_post_video = True
                        break

                estudiante.registrar_interaccion(mensaje, respuesta)
                with open(archivo, "a", encoding="utf-8") as log:
                    log.write(f"Usuario: {mensaje}\n")
                    log.write(f"Asistente: {respuesta}\n")
                    log.write("-"*30 + "\n")
            else:
                self.voz.hablar("\nLo siento, no entendí eso. ¿Puedes decirlo de otra manera?")


# --- Punto de entrada del programa ---
if __name__ == "__main__":
    bot = ChatBot()
    bot.iniciar()