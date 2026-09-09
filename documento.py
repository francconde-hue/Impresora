class Documento:
    def __init__(self, nombre, numero_paginas, tiempo_por_pagina):
        self.nombre = nombre
        self.numero_paginas = int(numero_paginas)
        self.tiempo_por_pagina = float(tiempo_por_pagina)