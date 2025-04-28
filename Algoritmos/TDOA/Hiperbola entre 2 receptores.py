# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 17:08:23 2025

@author: victo
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D  # Importamos para crear la línea de leyenda manual

# Parámetros del escenario
c = 1480  # Velocidad del sonido en agua (m/s)
pos_A = np.array([0, 0])     # Receptor A
pos_B = np.array([10, 0])    # Receptor B

# Supongamos tiempos inventados de llegada (en segundos)
t_A = 0.015  # tiempo en que A recibe la señal
t_B = 0.017  # tiempo en que B recibe la señal

# Calculamos la diferencia de tiempo de llegada
delta_t = t_A - t_B
delta_d = c * delta_t  # diferencia de distancia entre A y B (con signo)

# Grid para evaluar la función de la hipérbola
x = np.linspace(-10, 20, 500)
y = np.linspace(-10, 10, 500)
X, Y = np.meshgrid(x, y)

# Distancias desde cada punto del grid a los receptores
dA_grid = np.sqrt((X - pos_A[0])**2 + (Y - pos_A[1])**2)
dB_grid = np.sqrt((X - pos_B[0])**2 + (Y - pos_B[1])**2)

# Ecuación de la hipérbola respetando el signo de delta_d
Z = (dA_grid - dB_grid) - delta_d

# Crear la figura
fig, ax = plt.subplots()

# Dibujamos solo la rama correcta (donde Z ≈ 0)
hiperbola = ax.contour(X, Y, Z, levels=[0], colors='blue')

# Dibujamos los receptores
ax.scatter(*pos_A, color='red', label='Receptor A')
ax.scatter(*pos_B, color='green', label='Receptor B')

# Creamos una línea manual para representar la hipérbola en la leyenda
hiperbola_line = Line2D([0], [0], color='blue', lw=2, label='Posibles ubicaciones del emisor')

# Configuramos la leyenda incluyendo los receptores y la hipérbola
ax.legend(handles=ax.get_legend_handles_labels()[0] + [hiperbola_line])

# Configuraciones del gráfico
ax.set_title("Hipérbola entre 2 receptores")
ax.set_xlabel("X (m)")
ax.set_ylabel("Y (m)")
ax.axis("equal")
ax.grid(True)
plt.show()
