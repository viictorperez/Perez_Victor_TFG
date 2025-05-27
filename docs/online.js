// main.js

const map = L.map('map').setView([41.38, 2.17], 13);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

let polyline = L.polyline([], { color: 'blue' }).addTo(map);
let points = []; // Guardar el historial de puntos
let circle = null;
let lastTimestamp = null;

async function fetchLatestLocation() {
  try {
    const response = await fetch('https://backend-tfg-qzd9.onrender.com/data');
    const data = await response.json();

    const lat = data.latitude;
    const lon = data.longitude;
    const time = data.timestamp;

    if (time === lastTimestamp) return; // Mismo timestamp, ignorar
    lastTimestamp = time;

    if (!isNaN(lat) && !isNaN(lon)) {
      document.getElementById('timestamp').textContent = new Date(time).toLocaleString();

      const latlng = [lat, lon];
      points.push({ timestamp: time, latitude: lat, longitude: lon });

      if (circle) map.removeLayer(circle);
      circle = L.circleMarker(latlng, { radius: 8, color: 'red' }).addTo(map);

      polyline.addLatLng(latlng);
      map.setView(latlng, 16);
    }
  } catch (err) {
    console.error("Error al obtener datos del backend:", err);
  }
}

function clearTrack() {
  points = [];
  polyline.setLatLngs([]);
  if (circle) {
    map.removeLayer(circle);
    circle = null;
  }
  document.getElementById('timestamp').textContent = '---';
  lastTimestamp = null;
}

function downloadCSV() {
  if (points.length === 0) return;
  const rows = ["timestamp,latitude,longitude"];
  for (const p of points) {
    rows.push(`${p.timestamp},${p.latitude},${p.longitude}`);
  }
  const blob = new Blob([rows.join('\n')], { type: 'text/csv' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'track.csv';
  a.click();
  URL.revokeObjectURL(url);
}

fetchLatestLocation();
setInterval(fetchLatestLocation, 30000);
