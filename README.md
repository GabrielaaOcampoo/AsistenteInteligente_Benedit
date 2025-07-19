# AsistenteInteligente_Benedit
Este proyecto, desarrollado en la Universidad Nacional de Chimborazo (UNACH) Ecuador, demuestra cómo la inteligencia artificial puede aplicarse tanto en la resolución de problemas técnicos como en el acompañamiento humano. Benedit es un asistente inteligente creado en Python que ofrece apoyo emocional básico.
Benedit es un Asistente inteligente desarrollado en Python, diseñado para interactuar con los usuarios mediante texto y voz.

BeneditProject

 chatbot_model.h5                 # Modelo entrenado de la red neuronal
 
 classes.pkl                      # Clases de etiquetas de las intenciones
 
 intents.json                     # Base de datos de intenciones (preguntas/respuestas)
 
 main.py                          # Script principal para ejecutar el chatbot
 
 respuestas.py                    # Módulo con respuestas predefinidas

 training.py                      # Entrena el modelo usando intents.json
 
 usuario.py                       # Maneja información del usuario
 
 voz.py                           # Procesamiento de voz (entrada y salida)
 
 words.pkl                        # Palabras usadas para el entrenamiento del modelo
 
 conversacion_*.txt               # Transcripciones de conversaciones de prueba
 
 __pycache__                     # Archivos compilados por Python

Requisitos
Asegúrate de tener Python 3.10 o superior. Luego, instala las dependencias necesarias:
pip install numpy tensorflow nltk

Cómo ejecutar el chatbot
Entrenar el modelo (opcional):
Si quieres reentrenar el modelo desde cero:
python training.py

Ejecutar el chatbot:
Para iniciar la conversación con Benedit:
python main.py

Funcionalidad de voz (opcional)
El archivo voz.py gestiona la entrada y salida por voz. Puedes modificarlo para usar bibliotecas como pyttsx3 o speech_recognition si deseas integrar esta funcionalidad.

Archivos de prueba
Se incluyen varios archivos de conversación (conversacion_*.txt) con transcripciones de pruebas realizadas por diferentes usuarios.

⚙️ Detalle Técnico del Proyecto
🧠 Algoritmo Principal
El chatbot Benedit utiliza una red neuronal secuencial de tipo feedforward construida con TensorFlow/Keras. Esta red se entrena con datos estructurados en intents.json, un archivo que contiene distintas intenciones (preguntas comunes) y sus respuestas asociadas.

Se utilizan técnicas de Procesamiento de Lenguaje Natural (NLP):

Tokenización: se fragmentan las frases en palabras.

Stemming (raíz léxica) con nltk: se reduce cada palabra a su forma base.

Bag of Words (BoW): para representar las frases como vectores numéricos.


🧩 Módulos del Proyecto
1. training.py – Entrenamiento del modelo
Este script:

Lee intents.json para extraer frases y etiquetas.

Procesa el texto con nltk.

Crea un modelo de red neuronal con Keras, con capas densas (Dense) y función de activación softmax.

Guarda el modelo entrenado en chatbot_model.h5, y las palabras y clases en words.pkl y classes.pkl.

💡 Técnicas: NLP, red neuronal multicapa, clasificación supervisada.


2. main.py – Controlador principal del chatbot
Este archivo es el punto de entrada para el usuario. Carga el modelo entrenado y:

Lee la entrada del usuario por consola.

Predice la intención de la frase.

Llama al módulo respuestas.py para seleccionar una respuesta adecuada.

Imprime la respuesta o la reproduce por voz si se habilita.

💡 Flujo de ejecución del chatbot desde entrada hasta respuesta.


3. respuestas.py – Gestor de respuestas
Este módulo contiene una función que devuelve respuestas adecuadas basadas en la etiqueta que se predice.

Carga intents.json.

Busca la respuesta según la intención predicha.

También puede gestionar respuestas dinámicas (por ejemplo, con datos del usuario).

💡 Separación de la lógica de diálogo para mantener código limpio.


4. usuario.py – Gestión del usuario
Define un objeto de usuario con atributos como:

Nombre

Edad

Género

Estado emocional

Esto permite personalizar las respuestas del chatbot.

💡 Modelo básico de usuario para empatía y contexto emocional.



5. voz.py – Interacción por voz (entrada/salida)
Este módulo incluye funciones para:

Convertir texto en voz (con pyttsx3 o similar).

Capturar entrada de voz (requiere librerías adicionales).

💡 Permite una experiencia más natural al usuario.
