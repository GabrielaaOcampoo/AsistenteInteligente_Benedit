# ---------------------------------------------------------
# training.py - ENTRENADOR DEL MODELO PARA BENEDIT
# ---------------------------------------------------------
# Este archivo entrena un modelo de red neuronal para identificar
# las intenciones del usuario basadas en el archivo intents.json.
# La salida es un modelo llamado 'chatbot_model.h5' y dos archivos
# .pkl que contienen el vocabulario (words) y las clases (intents).
# ---------------------------------------------------------

# --- Librerías necesarias ---
import json              # Leer y manipular archivos JSON
import pickle            # Guardar estructuras de Python como archivos binarios
import random            # Aleatorizar datos de entrenamiento
import numpy as np       # Biblioteca para cálculos numéricos
import nltk              # Biblioteca para procesamiento de lenguaje natural
from nltk.stem import WordNetLemmatizer  # Reduce palabras a su forma base

# Componentes de Keras para construir y entrenar el modelo
from keras.models import Sequential         # Modelo secuencial (capa por capa)
from keras.layers import Dense, Dropout     # Capas densas y de eliminación (Dropout)
from keras.optimizers import SGD            # Optimizador: Stochastic Gradient Descent

# Descargar tokenizador de NLTK (si no está)
nltk.download('punkt')

# ---------------------------------------------------------
# Clase EntrenadorChatbot: organiza todo el proceso
# desde la lectura del JSON hasta el entrenamiento y guardado del modelo
# ---------------------------------------------------------
class EntrenadorChatbot:
    def __init__(self, intents_path='intents.json'):
        self.intents_path = intents_path        # Ruta del archivo JSON con los intents
        self.words = []                         # Lista del vocabulario (tokens únicos)
        self.classes = []                       # Lista de las diferentes clases (tags)
        self.documents = []                     # Lista de pares (tokens, tag)
        self.ignore_words = ['?', '!', '.', ',', '¡', '¿']  # Palabras a ignorar
        self.lemmatizer = WordNetLemmatizer()   # Objeto para lematizar palabras
        self.model = None                       # Lugar donde se guardará el modelo

    def cargar_datos(self):
        # Lee el archivo intents.json y lo guarda como diccionario
        with open(self.intents_path, encoding='utf-8') as f:
            self.intents = json.load(f)

    def procesar_datos(self):
        # Itera sobre cada intent
        for intent in self.intents['intents']:
            for pattern in intent['patterns']:
                # Tokeniza cada patrón en palabras individuales
                tokens = nltk.word_tokenize(pattern.lower())
                self.words.extend(tokens)  # Agrega palabras al vocabulario
                self.documents.append((tokens, intent['tag']))  # Asocia tokens con su etiqueta
                if intent['tag'] not in self.classes:
                    self.classes.append(intent['tag'])  # Agrega nueva clase

        # Limpieza: lematización y eliminación de puntuaciones
        self.words = [self.lemmatizer.lemmatize(w) for w in self.words if w not in self.ignore_words]
        self.words = sorted(set(self.words))      # Elimina duplicados y ordena alfabéticamente
        self.classes = sorted(set(self.classes))  # Ordena las clases

        # Guarda el vocabulario y las clases en archivos binarios para uso futuro
        pickle.dump(self.words, open('words.pkl', 'wb'))
        pickle.dump(self.classes, open('classes.pkl', 'wb'))

    def crear_datos_entrenamiento(self):
        training = []                              # Lista para los datos de entrenamiento
        output_empty = [0] * len(self.classes)     # Plantilla de salida (vector one-hot)

        for doc in self.documents:
            bag = []                               # Lista para Bag of Words de un patrón
            pattern_words = [self.lemmatizer.lemmatize(w.lower()) for w in doc[0]]  # Lematizar tokens

            for w in self.words:
                bag.append(1 if w in pattern_words else 0)  # Crear vector binario BoW

            # Vector de salida (one-hot)
            output_row = output_empty[:]
            output_row[self.classes.index(doc[1])] = 1      # Activar la clase correspondiente

            # Guardar patrón con su clase
            training.append([bag, output_row])

        # Mezclar aleatoriamente los datos
        random.shuffle(training)

        training = np.array(training, dtype=object)
        # Dividir en datos de entrada (X) y salida (Y)
        self.train_x = list(training[:, 0])    # Entradas: vectores BoW
        self.train_y = list(training[:, 1])    # Salidas: vectores one-hot

    def construir_modelo(self):
        # Construye la arquitectura de la red neuronal
        self.model = Sequential()
        self.model.add(Dense(256, input_shape=(len(self.train_x[0]),), activation='relu'))  # Capa de entrada
        self.model.add(Dropout(0.5))             # Dropout para evitar sobreajuste
        self.model.add(Dense(128, activation='relu'))  # Capa oculta
        self.model.add(Dropout(0.3))             # Segundo Dropout
        self.model.add(Dense(len(self.train_y[0]), activation='softmax'))  # Capa de salida con activación softmax

        # Configura el optimizador SGD (descenso por gradiente)
        sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
        self.model.compile(
            loss='categorical_crossentropy',  # Función de pérdida para clasificación múltiple
            optimizer=sgd,
            metrics=['accuracy']
        )

    def entrenar_modelo(self, epochs=300, batch_size=5):
        # Entrena el modelo con los datos procesados
        self.model.fit(
            np.array(self.train_x),     # Entradas
            np.array(self.train_y),     # Salidas
            epochs=epochs,              # Número de pasadas completas por los datos
            batch_size=batch_size,      # Tamaño de los lotes
            verbose=1                   # Mostrar progreso por consola
        )
        self.model.save('chatbot_model.h5')  # Guarda el modelo entrenado
        print("✅ Modelo entrenado y guardado como 'chatbot_model.h5'.")

    def entrenar(self):
        # Proceso completo para preparar y entrenar el modelo
        self.cargar_datos()             # Paso 1: Cargar archivo intents.json
        self.procesar_datos()           # Paso 2: Extraer vocabulario y clases
        self.crear_datos_entrenamiento()# Paso 3: Crear BoW y vectores de salida
        self.construir_modelo()         # Paso 4: Definir estructura de red neuronal
        self.entrenar_modelo()          # Paso 5: Entrenar la red con los datos

# --- Punto de entrada del script ---
if __name__ == "__main__":
    entrenador = EntrenadorChatbot()   # Crear instancia del entrenador
    entrenador.entrenar()              # Ejecutar proceso completo de entrenamiento