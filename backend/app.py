from flask import Flask, jsonify
import csv

app = Flask(__name__)

@app.route('/')
def home():
    return "Servidor funcionando"

@app.route('/data.json')
def devolver_json():
    datos = []
    with open('coordenadas.csv', newline='') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            datos.append({
                'timestamp': fila['timestamp'],
                'latitud': float(fila['latitud']),
                'longitud': float(fila['longitud']),
            })
    return jsonify(datos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
