from flask import Flask, jsonify
from flask_cors import CORS
import threading
import time
import random
from datetime import datetime
import csv
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s - %(message)s')

app = Flask(__name__)
CORS(app, origins=["https://viictorperez.github.io"])

ARCHIVO_CSV = 'coordenadas.csv'

def inicializar_csv():
    if not os.path.exists(ARCHIVO_CSV):
        with open(ARCHIVO_CSV, 'w', newline='') as archivo:
            writer = csv.writer(archivo)
            writer.writerow(['timestamp', 'latitud', 'longitud'])
        logging.info("✅ coordenadas.csv creado")

def generar_datos():
    while True:
        now = datetime.now().isoformat()
        base_lat, base_lon = -34.6037, -58.3816
        lat = base_lat + random.uniform(-0.01, 0.01)
        lon = base_lon + random.uniform(-0.01, 0.01)
        try:
            with open(ARCHIVO_CSV, 'a', newline='') as archivo:
                writer = csv.writer(archivo)
                writer.writerow([now, lat, lon])
            logging.info(f"🛰️ Punto generado: {lat}, {lon}")
        except Exception as e:
            logging.error(f"❌ Error escribiendo CSV: {e}")
        time.sleep(30)

@app.route('/')
def home():
    return "🛰️ Backend funcionando"

@app.route('/data.json')
def data_json():
    datos = []
    try:
        with open(ARCHIVO_CSV, newline='') as archivo:
            reader = csv.DictReader(archivo)
            for fila in reader:
                if 'timestamp' in fila:
                    datos.append({
                        'timestamp': fila['timestamp'],
                        'latitud': float(fila['latitud']),
                        'longitud': float(fila['longitud'])
                    })
        logging.info(f"📤 {len(datos)} puntos enviados a /data.json")
    except Exception as e:
        logging.error(f"❌ Error leyendo CSV: {e}")
    return jsonify(datos)

@app.route('/csv')
def ver_csv_como_texto():
    try:
        with open(ARCHIVO_CSV, 'r') as archivo:
            contenido = archivo.read()
        return f"<pre>{contenido}</pre>"
    except Exception as e:
        logging.error(f"❌ Error al leer CSV para /csv: {e}")
        return f"Error al leer CSV: {e}"

if __name__ == '__main__':
    inicializar_csv()

    hilo = threading.Thread(target=generar_datos, daemon=True)
    hilo.start()
    logging.info("🚀 Generador de coordenadas iniciado")

    app.run(host='0.0.0.0', port=10000)
