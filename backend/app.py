from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from typing import List
import uvicorn

app = FastAPI()

data_store = []

@app.post("/ttn") 
async def receive_ttn_webhook(request: Request):
    payload = await request.json()
    decoded = payload.get("uplink_message", {}).get("decoded_payload", {})
    timestamp = decoded.get("timestamp")
    latitude = decoded.get("latitude")
    longitude = decoded.get("longitude")

    entry = {
        "timestamp": timestamp,
        "latitude": latitude,
        "longitude": longitude
    }

    data_store.append(entry)
    if len(data_store) > 50:
        data_store.pop(0)

    return {"status": "ok"}

@app.get("/data")
def get_latest_data():
    if not data_store:
        return JSONResponse(status_code=404, content={"error": "No hay datos"})
    return data_store[-1]

@app.get("/")
def home():
    return {"mensaje": "FastAPI funcionando. Usa /ttn y /data"}
