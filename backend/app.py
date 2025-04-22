from flask import Flask, jsonify
from flask_cors import CORS
import threading
import time
import random
from datetime import datetime
import csv
import os

app = Flask(__name__)

# 🔒 Solo permitir solicitudes desde tu GitHub Pages
CORS(app, origins=["https://viictorperez.github.io"])

ARCHIVO_CSV = 'coordenadas.csv'


# Crear CSV con encabezado si no existe
def inicializar_csv():
    if not os.path.exists(ARCHIVO_CSV):
        with open(ARCHIVO_CSV, 'w', newline='') as archivo:
            writer = csv.writer(archivo)
            writer.writerow(['timestamp', 'latitud', 'longitud'])

# Generar un punto GPS cada 30 segundos
def generar_datos():
    while True:
        now = datetime.now().isoformat()
        base_lat, base_lon = -34.6037, -58.3816  # Buenos Aires
        lat = base_lat + random.uniform(-0.01, 0.01)
        lon = base_lon + random.uniform(-0.01, 0.01)
        with open(ARCHIVO_CSV, 'a', newline='') as archivo:
            writer = csv.writer(archivo)
            writer.writerow([now, lat, lon])
        print(f"[{now}] Punto generado: {lat}, {lon}")
        time.sleep(30)

@app.route('/')
def home():
    return "🛰️ Backend de puntos GPS en vivo"

@app.route('/data.json')
def data_json():
    datos = []
    try:
        with open(ARCHIVO_CSV, newline='') as archivo:
            reader = csv.DictReader(archivo)
            for fila in reader:
                datos.append({
                    'timestamp': fila['timestamp'],
                    'latitud': float(fila['latitud']),
                    'longitud': float(fila['longitud'])
                })
    except FileNotFoundError:
        pass  # Devuelve lista vacía si aún no existe
    return jsonify(datos)

# Iniciar generador de datos al arrancar la app
if __name__ == '__main__':
    inicializar_csv()
    threading.Thread(target=generar_datos, daemon=True).start()
    app.run(host='0.0.0.0', port=10000)
