import tkinter as tk
from tkinter import messagebox
from documento import Documento
from impresora import ColaImpresion

class InterfazImpresora:
    def __init__(self, root):
        self.root = root
        self.root.title("Impresora")
        self.root.geometry("600x550")
        
        
        self.sistema_impresion = ColaImpresion()
        self.id_after = None  

        
        tk.Label(root, text="Nombre del Documento:", font=("Arial", 10, "bold")).pack(pady=2)
        self.entry_nombre = tk.Entry(root, width=35)
        self.entry_nombre.pack()

        tk.Label(root, text="Número de Páginas:", font=("Arial", 10, "bold")).pack(pady=2)
        self.entry_paginas = tk.Entry(root, width=35)
        self.entry_paginas.pack()

        tk.Label(root, text="Tiempo por Página (segundos):", font=("Arial", 10, "bold")).pack(pady=2)
        self.entry_tiempo = tk.Entry(root, width=35)
        self.entry_tiempo.pack()

        # creacion de botones de la interfaz
        self.btn_agregar = tk.Button(root, text="Crear domumento", command=self.agregar, width=30)
        self.btn_agregar.pack(pady=8)

        self.btn_iniciar = tk.Button(root, text="Imprimir", command=self.iniciar_simulacion, width=30)
        self.btn_iniciar.pack(pady=4)

        self.btn_detener = tk.Button(root, text="Detener Impresión", command=self.detener_simulacion, width=30)
        self.btn_detener.pack(pady=4)

        # espacio donde se muestra la lista en cola y el estado de la impresion
        tk.Label(root, text="Monitor de sucesos:", font=("Arial", 10, "bold")).pack(pady=5)
        self.texto_estado = tk.Text(root, height=14, width=70)
        self.texto_estado.pack(pady=5)

    def agregar(self):
        nombre = self.entry_nombre.get().strip()
        paginas = self.entry_paginas.get().strip()
        tiempo = self.entry_tiempo.get().strip()

        if not nombre or not paginas or not tiempo:
            messagebox.showerror("Advertencia", "debe diligenciar todos los espacios.")
            return

        try:
            num_p = int(paginas)
            t_p = float(tiempo)
            
            # Creamos documento
            nuevo_doc = Documento(nombre, num_p, t_p)
            
            # Lo agregamos a la cola usando nuestra clase lógica
            self.sistema_impresion.agregar_documento(nuevo_doc)
            
            self.texto_estado.insert(tk.END, f"Se ha creado el documento: '{nombre}' ({num_p} págs) añadido a la cola.\n")
            self.texto_estado.see(tk.END)

            # despues de creado un documento se borra lo que haya escrito en los campos de texto
            self.entry_nombre.delete(0, tk.END)
            self.entry_paginas.delete(0, tk.END)
            self.entry_tiempo.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Error", "El número de páginas debe ser entero y el tiempo un número válido.")

    def iniciar_simulacion(self):
        if not self.sistema_impresion.imprimiendo:
            self.sistema_impresion.imprimiendo = True
            self.texto_estado.insert(tk.END, " Imprimiendo. \n")
            self.procesar_impresion()

    def detener_simulacion(self):
        self.sistema_impresion.imprimiendo = False
        if self.id_after:
            self.root.after_cancel(self.id_after)
            self.id_after = None
        self.texto_estado.insert(tk.END, " Se ha detenido la impresión. \n")
        self.texto_estado.see(tk.END)

    def procesar_impresion(self):
        if not self.sistema_impresion.imprimiendo:
            return

        # Si no hay documento actual imprimiéndose, sacamos el siguiente de la cola
        if self.sistema_impresion.documento_actual is None:
            if self.sistema_impresion.hay_documentos():
                doc = self.sistema_impresion.obtener_siguiente()
                self.texto_estado.insert(tk.END, f">> Imrpimeindo el primer documento en cola: '{doc.nombre}' ({doc.numero_paginas} páginas)\n")
            else:
                self.texto_estado.insert(tk.END, "No hay documentos en cola, Impresión finalizada...\n")
                self.sistema_impresion.imprimiendo = False
                return

        doc_act = self.sistema_impresion.documento_actual

        if doc_act:
            if self.sistema_impresion.pagina_actual < doc_act.numero_paginas:
                self.sistema_impresion.pagina_actual += 1
                self.texto_estado.insert(tk.END, f"   Imprimiendo: '{doc_act.name if hasattr(doc_act, 'name') else doc_act.nombre}' - Página {self.sistema_impresion.pagina_actual} de {doc_act.numero_paginas}\n")
                self.texto_estado.see(tk.END)
                
                # Convertimos el tiempo por página a milisegundos para el temporizador de Tkinter
                tiempo_ms = int(doc_act.tiempo_por_pagina * 1000)
                self.id_after = self.root.after(tiempo_ms, self.procesar_impresion)
            else:
                self.texto_estado.insert(tk.END, f"✔ ¡Documento '{doc_act.nombre}' impreso completamente!\n\n")
                self.texto_estado.see(tk.END)
                # Liberamos el documento actual para que tome el siguiente en el próximo ciclo
                self.sistema_impresion.documento_actual = None
                self.sistema_impresion.pagina_actual = 0
                self.id_after = self.root.after(100, self.procesar_impresion)

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazImpresora(root)
    root.mainloop()