from collections import deque

class ColaImpresion:
    def __init__(self):
        self.cola = deque()  # Cola basada en deque
        self.documento_actual = None
        self.pagina_actual = 0
        self.imprimiendo = False

    def agregar_documento(self, documento):
        #agrega un documento a la cola
        self.cola.append(documento)

    def obtener_siguiente(self):
        #toma el primer documento de la cola y lo deja como el actual para imprimir
        if self.cola:
            self.documento_actual = self.cola.popleft()
            self.pagina_actual = 0
            return self.documento_actual
        return None

    def hay_documentos(self):
        #realiza un barrido para ver si quedan documentos en cola
        return len(self.cola) > 0

    def limpiar_cola(self):
        #Limpia lo que halla en cola y reinicia el documento actual y la pagina actual
        self.cola.clear()
        self.documento_actual = None
        self.pagina_actual = 0