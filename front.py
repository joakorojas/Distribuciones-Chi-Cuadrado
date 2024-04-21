import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from back import generador_uniforme_a_b, calcular_chi_cuadrado
from back import generador_histograma
from back import generador_exponencial
from back import generador_normal
from back import mostrar_tabla_frecuencias



def mostrar_campos(opcion_seleccionada, ventana_principal):
    ventana_datos = tk.Toplevel(ventana_principal)
    ventana_datos.title("Ingrese los datos")

    if opcion_seleccionada == "Uniforme":
        etiqueta_cantidad = tk.Label(ventana_datos, text="Cantidad de números a generar:")
        etiqueta_cantidad.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        entrada_cantidad = tk.Entry(ventana_datos)
        entrada_cantidad.grid(row=0, column=1, padx=10, pady=5)

        etiqueta_a = tk.Label(ventana_datos, text="Valor de A:")
        etiqueta_a.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        entrada_a = tk.Entry(ventana_datos)
        entrada_a.grid(row=1, column=1, padx=10, pady=5)

        etiqueta_b = tk.Label(ventana_datos, text="Valor de B:")
        etiqueta_b.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        entrada_b = tk.Entry(ventana_datos)
        entrada_b.grid(row=2, column=1, padx=10, pady=5)

        def generar_uniforme():
            try:
                cantidad = int(entrada_cantidad.get())
                a = float(entrada_a.get())
                b = float(entrada_b.get())
                if cantidad <= 0 or cantidad > 1000000:
                    messagebox.showerror("Error", "La cantidad de números debe estar entre 1 y 1 millón")
                elif a >= b:
                    messagebox.showerror("Error", "El valor de A debe ser menor que el valor de B")
                else:
                    numeros_generados = generador_uniforme_a_b(cantidad, a, b)
                    mostrar_resultados(numeros_generados)
            except ValueError:
                messagebox.showerror("Error", "Por favor, ingrese números válidos")

        boton_generar = tk.Button(ventana_datos, text="Generar", command=generar_uniforme)
        boton_generar.grid(row=3, columnspan=2, padx=10, pady=10)

    elif opcion_seleccionada == "Exponencial":
        etiqueta_cantidad = tk.Label(ventana_datos, text="Cantidad de números a generar:")
        etiqueta_cantidad.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        entrada_cantidad = tk.Entry(ventana_datos)
        entrada_cantidad.grid(row=0, column=1, padx=10, pady=5)

        etiqueta_lambda = tk.Label(ventana_datos, text="Tasa de llegada (λ):")
        etiqueta_lambda.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        entrada_lambda = tk.Entry(ventana_datos)
        entrada_lambda.grid(row=1, column=1, padx=10, pady=5)

        def generar_exponencial():
                global lambd
                lambd = None
                cantidad = int(entrada_cantidad.get())
                lambd = float(entrada_lambda.get())
                if cantidad <= 0 or cantidad > 1000000:
                    messagebox.showerror("Error", "La cantidad de números debe estar entre 1 y 1 millón")
                elif lambd <= 0:
                    messagebox.showerror("Error", "La tasa de llegada (λ) debe ser mayor que cero")
                else:
                    # Llama a la función generador_exponencial y muestra los datos en una nueva ventana
                    numeros_generados = generador_exponencial(cantidad, lambd)
                    mostrar_resultados(numeros_generados)

        boton_generar = tk.Button(ventana_datos, text="Generar", command=generar_exponencial)
        boton_generar.grid(row=3, columnspan=2, padx=10, pady=10)

    elif opcion_seleccionada == "Normal":
        etiqueta_cantidad = tk.Label(ventana_datos, text="Cantidad de números a generar:")
        etiqueta_cantidad.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        entrada_cantidad = tk.Entry(ventana_datos)
        entrada_cantidad.grid(row=0, column=1, padx=10, pady=5)

        etiqueta_media = tk.Label(ventana_datos, text="Media:")
        etiqueta_media.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        entrada_media = tk.Entry(ventana_datos)
        entrada_media.grid(row=1, column=1, padx=10, pady=5)

        etiqueta_desviacion = tk.Label(ventana_datos, text="Desviación estándar:")
        etiqueta_desviacion.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        entrada_desviacion = tk.Entry(ventana_datos)
        entrada_desviacion.grid(row=2, column=1, padx=10, pady=5)

        def generar_normal():
            try:
                global media
                global desviacion 
                cantidad = int(entrada_cantidad.get())
                media = float(entrada_media.get())
                desviacion = float(entrada_desviacion.get())
                if cantidad <= 0 or cantidad > 1000000:
                    messagebox.showerror("Error", "La cantidad de números debe estar entre 1 y 1 millón")
                elif desviacion <= 0:
                    messagebox.showerror("Error", "La desviación estándar debe ser mayor que cero")
                else:
                    numeros_generados = generador_normal(cantidad, media, desviacion)
                    mostrar_resultados(numeros_generados)
            except ValueError:
                messagebox.showerror("Error", "Por favor, ingrese números válidos")

        boton_generar = tk.Button(ventana_datos, text="Generar", command=generar_normal)
        boton_generar.grid(row=3, columnspan=2, padx=10, pady=10)

def mostrar_ventana_datos():
    global opcion_seleccionada
    opcion_seleccionada = seleccion.get()
    mostrar_campos(opcion_seleccionada, ventana_principal)

def mostrar_resultados(numeros_generados):
    ventana_resultados = tk.Toplevel(ventana_principal)
    ventana_resultados.title("Resultados")

    lista_numeros = tk.Listbox(ventana_resultados)
    lista_numeros.pack(padx=10, pady=10)

    for i, numero in enumerate(numeros_generados, start=1):
        texto_resultado = f"{i}:    {numero}"
        lista_numeros.insert(tk.END, texto_resultado)

    boton_histograma = tk.Button(ventana_resultados, text="Generar Histograma", command=lambda: ventana_intervalos(numeros_generados))
    boton_histograma.pack(padx=10, pady=10)

def ventana_intervalos(numeros_generados):
    ventana_histograma = tk.Toplevel(ventana_principal)
    ventana_histograma.title("Generar Histograma")

    etiqueta_intervalos = tk.Label(ventana_histograma, text="Cantidad intervalos:")
    etiqueta_intervalos.grid(row=0, column=0, padx=10, pady=10, sticky="w") 
    opciones_intervalos = [10, 15, 20, 25]
    seleccion_intervalos = ttk.Combobox(ventana_histograma, values=opciones_intervalos, state='readonly')
    seleccion_intervalos.grid(row=0, column=1, padx=10, pady=10)

    def generar_histograma():
        intervalos = int(seleccion_intervalos.get())
        if opcion_seleccionada == 'Exponencial':
            frecuencias_uniformes = generador_histograma(intervalos, numeros_generados, opcion_seleccionada, lambd)
        elif opcion_seleccionada == 'Normal':
            frecuencias_uniformes = generador_histograma(intervalos, numeros_generados, opcion_seleccionada, None, media, desviacion)
        else:
            frecuencias_uniformes = generador_histograma(intervalos, numeros_generados, opcion_seleccionada)
        mostrar_tabla_frecuencias(frecuencias_uniformes)

        # Agregar botón para la Prueba Chi Cuadrado
        boton_prueba_chi_cuadrado = tk.Button(ventana_histograma, text="Prueba Chi Cuadrado", command=lambda: realizar_prueba_chi_cuadrado(frecuencias_uniformes))
        boton_prueba_chi_cuadrado.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    boton_generar = tk.Button(ventana_histograma, text="Generar", command=generar_histograma)
    boton_generar.grid(row=0, column=2, padx=10, pady=10)

    
#Tabla que muestra el chi calculado
def realizar_prueba_chi_cuadrado(frecuencias):
    chi_cuadrado = calcular_chi_cuadrado(frecuencias)
    messagebox.showinfo("Resultado Prueba Chi Cuadrado", f"El Ji Cuadrado calculado  es: {chi_cuadrado}")

ventana_principal = tk.Tk()
ventana_principal.title("Generador de números aleatorios")

etiqueta_distribucion = tk.Label(ventana_principal, text="Distribución:")
etiqueta_distribucion.grid(row=0, column=0, padx=10, pady=10, sticky="w")
opciones = ["Uniforme", "Exponencial", "Normal"]
seleccion = ttk.Combobox(ventana_principal, values=opciones, state='readonly')
seleccion.grid(row=0, column=1, padx=10, pady=10)

boton_siguiente = tk.Button(ventana_principal, text="Siguiente", command=mostrar_ventana_datos)
boton_siguiente.grid(row=0, column=2, padx=10, pady=10)

ventana_principal.mainloop()