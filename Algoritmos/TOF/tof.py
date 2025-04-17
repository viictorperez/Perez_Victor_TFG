# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 11:42:35 2025

@author: victo
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import least_squares

def trilateration(positions, distances):
    def equations(vars, positions, distances):
        x, y = vars
        return [(np.sqrt((x - px) ** 2 + (y - py) ** 2) - d) for (px, py), d in zip(positions, distances)]
    
    # Estimación inicial del emisor
    x0, y0 = np.mean(positions, axis=0)
    result = least_squares(equations, [x0, y0], args=(positions, distances))
    return result.x

def plot_trilateration(positions, distances, emisor_pos):
    fig, ax = plt.subplots()
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title("Trilateración - Posición del Emisor")
    
    # Dibujar círculos de distancia
    for (px, py), d in zip(positions, distances):
        circle = plt.Circle((px, py), d, color='b', fill=False, linestyle='dashed')
        ax.add_patch(circle)
        ax.scatter(px, py, color='r', label="Receptor" if 'Receptor' not in ax.get_legend_handles_labels()[1] else "")
    
    # Dibujar el emisor
    ax.scatter(*emisor_pos, color='g', marker='x', s=100, label="Emisor")
    
    ax.set_xlim(min(positions[:,0]) - max(distances), max(positions[:,0]) + max(distances))
    ax.set_ylim(min(positions[:,1]) - max(distances), max(positions[:,1]) + max(distances))
    ax.legend()
    plt.grid()
    plt.show()

# Cargar el archivo Excel
df = pd.read_excel("csvtof.xlsx")

# Extraer datos de los receptores
positions = df[['x', 'y']].values
distances = df['rango'].values

# Calcular la posición del emisor
emisor_pos = trilateration(positions, distances)
print(f"Posición estimada del emisor: x={emisor_pos[0]:.2f}, y={emisor_pos[1]:.2f}")

# Graficar los resultados
plot_trilateration(positions, distances, emisor_pos)
