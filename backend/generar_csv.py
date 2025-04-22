import csv
import time
from datetime import datetime
import random

ARCHIVO_CSV = 'coordenadas.csv'

def crear_csv_si_no_existe():
    try:
        with open(ARCHIVO_CSV, 'x', newline='') as archivo:
            writer = csv.writer(archivo)
            writer.writerow(['timestamp', 'latitud', 'longitud'])
    except FileExistsError:
        pass  # ya existe

def generar_datos_gps():
    # Simula coordenadas cerca de un punto base
    base_lat, base_lon = -34.6037, -58.3816  # Buenos Aires
    lat = base_lat + random.uniform(-0.01, 0.01)
    lon = base_lon + random.uniform(-0.01, 0.01)
    return lat, lon

def agregar_fila_csv():
    now = datetime.now().isoformat()
    lat, lon = generar_datos_gps()
    with open(ARCHIVO_CSV, 'a', newline='') as archivo:
        writer = csv.writer(archivo)
        writer.writerow([now, lat, lon])
    print(f"[{now}] Coordenada guardada: {lat}, {lon}")

def loop_principal():
    crear_csv_si_no_existe()
    while True:
        agregar_fila_csv()
        time.sleep(60)

if __name__ == '__main__':
    loop_principal()
