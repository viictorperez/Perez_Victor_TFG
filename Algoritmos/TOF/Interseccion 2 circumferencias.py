# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 21:02:06 2025

@author: victo
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# Parámetros
c = 1480  # Velocidad del sonido en agua (m/s)

# Posiciones de los receptores
pos_A = np.array([0, 0])
pos_B = np.array([10, 0])


# Tiempos de vuelo
tof_A = 0.00363862
tof_B = 0.00363862

# A partir de los tiempos de vuelo, recalculamos distancias
d_A = c * tof_A
d_B = c * tof_B


print(f"TOF_A: {tof_A:.8f} s, Distancia A: {d_A:.2f} m")
print(f"TOF_B: {tof_B:.8f} s, Distancia B: {d_B:.2f} m")

# Grid para evaluar las funciones
x = np.linspace(-10, 20, 500)
y = np.linspace(-10, 20, 500)
X, Y = np.meshgrid(x, y)

# Ecuaciones de las circunferencias
circle_A = (X - pos_A[0])**2 + (Y - pos_A[1])**2 - d_A**2
circle_B = (X - pos_B[0])**2 + (Y - pos_B[1])**2 - d_B**2

# Crear la figura
fig, ax = plt.subplots()

# Dibujar las circunferencias
circ_A = ax.contour(X, Y, circle_A, levels=[0], colors='red')
circ_B = ax.contour(X, Y, circle_B, levels=[0], colors='blue')

# Dibujar los receptores y el emisor real
ax.scatter(*pos_A, color='red', label='Receptor A')
ax.scatter(*pos_B, color='blue', label='Receptor B')

# Configurar leyenda
custom_lines = [
    Line2D([0], [0], color='red', lw=2, label='Circunferencia A'),
    Line2D([0], [0], color='blue', lw=2, label='Circunferencia B'),
]
ax.legend(handles=ax.get_legend_handles_labels()[0] + custom_lines)

# Configuraciones del gráfico
ax.set_title("Intersección de cirunferencias con 2 receptores")
ax.set_xlabel("X (m)")
ax.set_ylabel("Y (m)")
ax.axis('equal')
ax.grid(True)
plt.show()
