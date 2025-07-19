
# CHATBOT Benedit, tu asistente emocional universitario 😊
# Este código define la clase Estudiante, que me ayuda a conocerte mejor
# y recordar cómo te has sentido durante nuestras conversaciones.

class Estudiante:
    # Método constructor: se ejecuta al crear una nueva instancia de la clase
    def __init__(self, nombre, semestre, paralelo):
        self.nombre = nombre              # Guarda el nombre del estudiante
        self.semestre = semestre          # Guarda el semestre actual del estudiante
        self.paralelo = paralelo          # Guarda el paralelo (grupo o sección) del estudiante
        self.historial = []               # Inicializa una lista vacía para registrar las interacciones

    # Método para registrar una interacción entre el estudiante y el asistente
    def registrar_interaccion(self, entrada, respuesta):
        self.historial.append((entrada, respuesta))  # Añade una tupla (entrada, respuesta) al historial