import random
import numpy as np
import matplotlib.pyplot as plt
import math
import tkinter as tk
from tkinter import ttk
from scipy.stats import norm
from tkinter import messagebox

class Frecuencia:
    def __init__(self, limite_inferior, limite_superior, frecuencia_observada, frecuencia_esperada):
        self.limite_inferior = round(float(limite_inferior), 4)
        self.limite_superior = round(float(limite_superior), 4)
        self.frecuencia_observada = round(float(frecuencia_observada), 4)
        self.frecuencia_esperada = round(float(frecuencia_esperada), 4)
    def __str__(self):
        return f"Límite Inferior: {self.limite_inferior:.4f}, " \
               f"Límite Superior: {self.limite_superior:.4f}, " \
               f"Frecuencia Observada: {self.frecuencia_observada:.4f}, " \
               f"Frecuencia Esperada: {self.frecuencia_esperada:.4f}"


def distribucion_exponencial_negativa(limite, lambdaE):
    """ Función para evaluar la distribución exponencial negativa en un punto x con parámetro lambdaE """
    return 1 - math.exp(-lambdaE * limite)

#Funcion para generar un numero aleatorio entre 0 y 1
def generador_nro_rnd():
    nro_rnd = random.random()
    return nro_rnd

#Funcion para generar x cantidad de numeros aleatoreos entre a y b utilizando el generador de numeros rnd
def generador_uniforme_a_b(cantidad, a, b):
    c = b - a
    listado = [round(a + generador_nro_rnd() * c,4) for _ in range(cantidad)]
    return listado

# Función para generar números aleatorios utilizando la distribución exponencial
def generador_exponencial(cantidad, lambd):
    numeros_generados = [round(-math.log(1 - generador_nro_rnd()) / lambd,4) for _ in range(cantidad)]
    return numeros_generados

def generador_normal(cantidad, media, desviacion):
    numeros_generados = []
    while len(numeros_generados) < cantidad:
        # Generar dos números aleatorios u1 y u2 en el rango (0, 1)
        u1 = 1 - generador_nro_rnd()  # Asegúrate de generar números en el rango (0, 1)
        u2 = 1 - generador_nro_rnd()
        
        # Calcular z1 y z2 usando la transformación de Box-Muller
        z1 = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
        z2 = math.sqrt(-2 * math.log(u1)) * math.sin(2 * math.pi * u2)
        
        # Agregar los números generados ajustados a la media y desviación estándar
        numeros_generados.append(round(media + desviacion * z1, 4))
        
        # Solo agregar z2 si no se ha alcanzado la cantidad deseada
        if len(numeros_generados) < cantidad:
            numeros_generados.append(round(media + desviacion * z2, 4))
    
    return numeros_generados



def generador_histograma(k, datos, opcion_seleccionada, lambd=None, media=None, desviacion=None):
    #n array de frecuencias observadas
    n, bins, _ = plt.hist(datos, bins=k, color='blue', edgecolor='black')

    # Calcular el ancho de cada intervalo
    bin_width = bins[1] - bins[0]

    # Calcular los límites inferiores y superiores de cada intervalo
    #Vector con los limites inferiores
    lower_limits = bins[:-1]
    #Vector con los limites superiores
    upper_limits = bins[1:]
    
    # Agregar etiquetas y título
    plt.xlabel('Valor')
    plt.ylabel('Frecuencia')
    plt.suptitle('Histograma de Distribución ' + opcion_seleccionada)
    # Agregar la amplitud justo debajo del título
    plt.title(f"Amplitud: {round(bin_width,4)}")    

    # Establecer las marcas y etiquetas del eje x con los límites inferiores y superiores
    plt.xticks(np.arange(lower_limits.min(), upper_limits.max() + bin_width, bin_width), rotation=45)
    
    # Mostrar el histograma
    plt.show()

    # Crear una lista para almacenar objetos Frecuencia
    frecuencias = []

    i = 0
    #Va iterando por cada intervalo
    while i < len(n):
        # Da los límites y la frecuencia observada del intervalo actual
        lower = lower_limits[i]
        upper = upper_limits[i]
        frecuencia_obs = n[i]

        # Calcula la frecuencia esperada según la distribución que tiene
        if opcion_seleccionada == "Uniforme":
            frecuencia_esperada = len(datos) / k

        elif opcion_seleccionada == "Exponencial":
            exp_negativa_LS = distribucion_exponencial_negativa(upper, lambd)
            exp_negativa_LI = distribucion_exponencial_negativa(lower, lambd)
            frecuencia_esperada = abs((exp_negativa_LS - exp_negativa_LI) * len(datos))

        elif opcion_seleccionada == 'Normal':
            if media is None or desviacion is None:
                raise ValueError("Para calcular la frecuencia esperada para una distribución normal, se requiere la media y la desviación estándar.")

            # Calcular la probabilidad acumulativa hasta los límites superior e inferior
            prob_inf = norm.cdf(lower, loc=media, scale=desviacion)
            prob_sup = norm.cdf(upper, loc=media, scale=desviacion)

            # Calcular la frecuencia esperada multiplicando por el total de datos generados
            frecuencia_esperada = (prob_sup - prob_inf) * len(datos)

        # Si la frecuencia esperada es menor a 5, fusionar con el intervalo siguiente
        while frecuencia_esperada < 5 and i < len(n) - 1:
            i += 1
            upper = upper_limits[i]
            frecuencia_obs += n[i]

            if opcion_seleccionada == "Exponencial":
                exp_negativa_LS = distribucion_exponencial_negativa(upper, lambd)
                exp_negativa_LI = distribucion_exponencial_negativa(lower, lambd)
                frecuencia_esperada = abs((exp_negativa_LS - exp_negativa_LI) * len(datos))
            elif opcion_seleccionada == 'Normal':
                prob_sup = norm.cdf(upper, loc=media, scale=desviacion)
                frecuencia_esperada = (prob_sup - prob_inf) * len(datos)

        frecuencia_obj = Frecuencia(lower, upper, frecuencia_obs, frecuencia_esperada)
        frecuencias.append(frecuencia_obj)
        
        

        i += 1
    return frecuencias
    

def mostrar_tabla_frecuencias(frecuencias):
    ventana_tabla = tk.Toplevel()
    ventana_tabla.title("Tabla de Frecuencias")

    tabla_frame = ttk.Frame(ventana_tabla)
    tabla_frame.pack(padx=10, pady=10)

    tabla = ttk.Treeview(tabla_frame, columns=('Límite Inferior', 'Límite Superior', 'Frecuencia Observada', 'Frecuencia Esperada'), show='headings')
    tabla.heading('Límite Inferior', text='Límite Inferior')
    tabla.heading('Límite Superior', text='Límite Superior')
    tabla.heading('Frecuencia Observada', text='Frecuencia Observada')
    tabla.heading('Frecuencia Esperada', text='Frecuencia Esperada')

    for frecuencia in frecuencias:
        limite_inf = frecuencia.limite_inferior
        limite_sup = frecuencia.limite_superior
        frec_obs = frecuencia.frecuencia_observada
        frec_esp = frecuencia.frecuencia_esperada
        tabla.insert('', 'end', values=(limite_inf, limite_sup, frec_obs, frec_esp))

    tabla.pack()

    # Verificar si alguna frecuencia esperada es menor a 5
    frecuencias_bajas = [f for f in frecuencias if f.frecuencia_esperada < 5]
    if frecuencias_bajas:
        #Agrupa los intervalos menores a 5
        fusionar_intervalos(frecuencias_bajas, tabla, frecuencias)



def fusionar_intervalos(frecuencias_bajas, tabla, frecuencias):
    # Fusión de intervalos
    for f in frecuencias_bajas:
        indice = frecuencias.index(f)
        if indice > 0:
            frecuencia_anterior = frecuencias[indice - 1]
            frecuencia_anterior.limite_superior = f.limite_superior
            frecuencia_anterior.frecuencia_observada += f.frecuencia_observada
            frecuencia_anterior.frecuencia_esperada += f.frecuencia_esperada
            # Eliminar la frecuencia actual
            frecuencias.remove(f)

    # Actualizar la tabla de frecuencias
    tabla.delete(*tabla.get_children())  # Limpiar la tabla actual
    for frecuencia in frecuencias:
        tabla.insert('', 'end', values=(frecuencia.limite_inferior, frecuencia.limite_superior, frecuencia.frecuencia_observada, frecuencia.frecuencia_esperada))

def calcular_chi_cuadrado(frecuencias):
    chi_cuadrado = 0
    for frecuencia in frecuencias:
        # Calcula el término del estadístico de Ji Cuadrado para cada intervalo
        chi_cuadrado += ((frecuencia.frecuencia_observada - frecuencia.frecuencia_esperada) ** 2) / frecuencia.frecuencia_esperada
    return round(chi_cuadrado, 4)

