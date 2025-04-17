# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 12:00:54 2025

@author: victo
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.optimize import least_squares

def trilateration_3d(positions, distances):
    def equations(vars, positions, distances):
        x, y, z = vars
        return [(np.sqrt((x - px) ** 2 + (y - py) ** 2 + (z - pz) ** 2) - d) for (px, py, pz), d in zip(positions, distances)]
    
    # Estimación inicial del emisor
    x0, y0, z0 = np.mean(positions, axis=0)
    result = least_squares(equations, [x0, y0, z0], args=(positions, distances))
    return result.x

def plot_trilateration_3d(positions, distances, emisor_pos):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("Trilateración 3D - Posición del Emisor")
    
    # Dibujar esferas de distancia
    u = np.linspace(0, 2 * np.pi, 30)
    v = np.linspace(0, np.pi, 15)
    for (px, py, pz), d in zip(positions, distances):
        x = px + d * np.outer(np.cos(u), np.sin(v))
        y = py + d * np.outer(np.sin(u), np.sin(v))
        z = pz + d * np.outer(np.ones(np.size(u)), np.cos(v))
        ax.plot_wireframe(x, y, z, color='b', alpha=0.3)
        ax.scatter(px, py, pz, color='r', label="Receptor" if 'Receptor' not in ax.get_legend_handles_labels()[1] else "")
    
    # Dibujar el emisor
    ax.scatter(*emisor_pos, color='g', marker='x', s=100, label="Emisor")
    ax.legend()
    plt.show()

# Cargar el archivo Excel
df = pd.read_excel("csvtof.xlsx")

# Extraer datos de los receptores
positions = df[['x', 'y', 'z']].values
distances = df['rango'].values

# Calcular la posición del emisor en 3D
emisor_pos = trilateration_3d(positions, distances)
print(f"Posición estimada del emisor: x={emisor_pos[0]:.2f}, y={emisor_pos[1]:.2f}, z={emisor_pos[2]:.2f}")

# Graficar los resultados
plot_trilateration_3d(positions, distances, emisor_pos)
