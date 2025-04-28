# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 17:31:29 2025

@author: victo
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# Parámetros del escenario
c = 1480  # Velocidad del sonido en agua (m/s)

# Definimos 3 receptores
pos_A = np.array([0, 0])
pos_B = np.array([10, 0])
pos_C = np.array([0, 10])

# Tiempos inventados de llegada (en segundos)
t_A = 0.015
t_B = 0.017
t_C = 0.016

# Calculamos las diferencias de tiempo respecto a A
delta_t_AB = t_A - t_B
delta_t_AC = t_A - t_C

# Convertimos diferencias de tiempo en diferencias de distancia
delta_d_AB = c * delta_t_AB
delta_d_AC = c * delta_t_AC

# Grid para evaluar la función de las hipérbolas
x = np.linspace(-10, 20, 500)
y = np.linspace(-10, 20, 500)
X, Y = np.meshgrid(x, y)

# Distancias desde cada punto del grid a los receptores
dA = np.sqrt((X - pos_A[0])**2 + (Y - pos_A[1])**2)
dB = np.sqrt((X - pos_B[0])**2 + (Y - pos_B[1])**2)
dC = np.sqrt((X - pos_C[0])**2 + (Y - pos_C[1])**2)

# Crear la figura
fig, ax = plt.subplots()

# Graficamos las dos hipérbolas (sin etiquetas directas)
hiperbola_AB = ax.contour(X, Y, (dA - dB) - delta_d_AB, levels=[0], colors='blue')
hiperbola_AC = ax.contour(X, Y, (dA - dC) - delta_d_AC, levels=[0], colors='orange')

# Dibujamos los receptores
ax.scatter(*pos_A, color='red', label='Receptor A')
ax.scatter(*pos_B, color='green', label='Receptor B')
ax.scatter(*pos_C, color='magenta', label='Receptor C')

# Crear líneas de leyenda para las hipérbolas
hiperbolas_legend = [
    Line2D([0], [0], color='blue', lw=2, label='Hipérbola A-B'),
    Line2D([0], [0], color='orange', lw=2, label='Hipérbola A-C')
]

# Añadir todo a la leyenda
ax.legend(handles=ax.get_legend_handles_labels()[0] + hiperbolas_legend)

# Configuraciones del gráfico
ax.set_title("Posición 2d con 3 receptores")
ax.set_xlabel("X (m)")
ax.set_ylabel("Y (m)")
ax.axis("equal")
ax.grid(True)
plt.show()
