from flask import Flask, jsonify
import os
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

TTN_API_KEY = os.getenv("TTN_API_KEY")
TTN_APP_ID = "mkrgpslora"  # cambia si tu app se llama diferente

@app.route("/data")
def get_data():
    url = f"https://eu1.cloud.thethings.network/api/v3/as/applications/{TTN_APP_ID}/packages/storage/uplink_message"
    headers = {
        "Authorization": f"Bearer {TTN_API_KEY}"
    }

    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        return jsonify(r.json())
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "No se pudo obtener datos de TTN"}), 500

@app.route("/")
def home():
    return "Servidor Flask funcionando. Ruta /data disponible."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 3000)))
