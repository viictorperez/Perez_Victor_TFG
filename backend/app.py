from flask import Flask, jsonify, request
import os
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

data_store = []  # Lista temporal para almacenar mensajes recibidos

@app.route("/ttn", methods=["POST"])
def receive_ttn_webhook():
    try:
        payload = request.get_json()
        print("Mensaje recibido desde TTN:", json.dumps(payload, indent=2))

        # Extraer campos clave del mensaje (ej. lat/lon/time si están presentes)
        decoded = payload.get("uplink_message", {}).get("decoded_payload", {})

        entry = {
            "timestamp": decoded.get ("timestamp"),
            "latitude": decoded.get("latitude"),
            "longitude": decoded.get("longitude")
        }

        data_store.append(entry)
        if len(data_store) > 50:
            data_store.pop(0)

        return "OK", 200
    except Exception as e:
        print("Error al procesar webhook:", e)
        return "Error", 400

@app.route("/data")
def get_latest_data():
    if not data_store:
        return jsonify({"error": "No hay datos disponibles"}), 404

    return jsonify(data_store[-1])

@app.route("/")
def home():
    return "Servidor Flask funcionando. Ruta /ttn para recibir, /data para leer."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 3000)))
