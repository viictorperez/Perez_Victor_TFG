# -*- coding: utf-8 -*-
"""
Created on Sat Mar  8 11:11:44 2025

@author: victo
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import itertools
from scipy.optimize import minimize

# Cargar el CSV (ajusta la ruta si es necesario)
file_path = "tdoa_receptores_con_posiciones.csv"
df = pd.read_csv(file_path)

# Velocidad del sonido en agua (m/s)
c = 1480

# Calcular diferencias de tiempo y distancias entre pares de receptores
pares = list(itertools.combinations(df.index, 2))
diferencias = []
for i, j in pares:
    receptor_i = df.iloc[i]
    receptor_j = df.iloc[j]

    delta_t = receptor_i["Tiempo de Recepción (s)"] - receptor_j["Tiempo de Recepción (s)"]
    delta_d = c * delta_t

    diferencias.append({
        "pos_i": (receptor_i["Posición X (m)"], receptor_i["Posición Y (m)"]),
        "pos_j": (receptor_j["Posición X (m)"], receptor_j["Posición Y (m)"]),
        "delta_d": delta_d
    })

# Definir función de error para encontrar el punto más cercano a las hipérbolas
def error_function(point):
    x, y = point
    error = 0
    for diff in diferencias:
        xi, yi = diff["pos_i"]
        xj, yj = diff["pos_j"]
        delta_d = diff["delta_d"]

        dist_i = np.sqrt((x - xi)**2 + (y - yi)**2)
        dist_j = np.sqrt((x - xj)**2 + (y - yj)**2)
        error += (dist_i - dist_j - delta_d)**2
    return error

# Optimización para encontrar el punto más probable
resultado = minimize(error_function, x0=(0, 0))

# Crear figura para graficar
plt.figure(figsize=(10, 8))

x_vals = np.linspace(-50, 60, 500)
y_vals = np.linspace(-50, 60, 500)
X, Y = np.meshgrid(x_vals, y_vals)

for diff in diferencias:
    xi, yi = diff["pos_i"]
    xj, yj = diff["pos_j"]
    delta_d = diff["delta_d"]

    D1 = np.sqrt((X - xi) ** 2 + (Y - yi) ** 2)
    D2 = np.sqrt((X - xj) ** 2 + (Y - yj) ** 2)
    Z = D1 - D2

    plt.contour(X, Y, Z, levels=[delta_d], linewidths=1.5, colors='red', linestyles='dashed')
    plt.text(xi, yi, f"({xi},{yi})", fontsize=8, color='blue', ha='right')
    plt.text(xj, yj, f"({xj},{yj})", fontsize=8, color='blue', ha='right')

# Graficar receptores
plt.scatter(df["Posición X (m)"], df["Posición Y (m)"], color='blue', marker='o', s=80, label='Receptores')

# Dibujar punto estimado del emisor
plt.scatter(resultado.x[0], resultado.x[1], color='green', marker='x', s=120, label='Emisor estimado')

plt.xlabel('X (m)')
plt.ylabel('Y (m)')
plt.title('Hipérbolas TDOA y posición estimada del emisor')
plt.grid(True)
plt.axis('equal')
plt.legend()
plt.show()

print(f"Posición estimada del emisor: X = {resultado.x[0]:.2f} m, Y = {resultado.x[1]:.2f} m")
