let map = null;
let marker = null;
let polyline = null;
let points = [];
let circle = null;
let lastTimestamp = null;

function initMap() {
  map = L.map('map').setView([41.38, 2.17], 13);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);

  marker = L.marker([0, 0]).addTo(map);
  polyline = L.polyline([], { color: 'blue' }).addTo(map);
}

async function fetchLatestLocation() {
  try {
    const response = await fetch('https://backend-tfg-qzd9.onrender.com/data');
    const data = await response.json();

    const lat = data.latitude;
    const lon = data.longitude;
    const time = data.timestamp;

    if (time === lastTimestamp) return;
    lastTimestamp = time;

    document.getElementById('timestamp').textContent = new Date(time).toLocaleString();

    const latlng = [lat, lon];
    points.push({ timestamp: time, latitude: lat, longitude: lon });

    if (circle) map.removeLayer(circle);
    circle = L.circleMarker(latlng, { radius: 8, color: 'red' }).addTo(map);

    polyline.addLatLng(latlng);
    marker.setLatLng(latlng);
    map.setView(latlng, 16);
  } catch (err) {
    console.error("Error al obtener datos del backend:", err);
  }
}

function clearTrack() {
  points = [];
  if (polyline) polyline.setLatLngs([]);
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

function mostrarSeccion(id) {
  const online = document.getElementById('online');
  const offline = document.getElementById('offline');

  online.style.display = (id === 'online') ? 'block' : 'none';
  offline.style.display = (id === 'offline') ? 'block' : 'none';

  if (id === 'online') {
    setTimeout(() => {
      if (!map) {
        initMap();
        fetchLatestLocation();
        setInterval(fetchLatestLocation, 30000);
      } else {
        map.invalidateSize();
      }
    }, 100);
  }
}

window.clearTrack = clearTrack;
window.downloadCSV = downloadCSV;
window.mostrarSeccion = mostrarSeccion;

// Por si online es la sección inicial visible:
window.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('online').style.display !== 'none') {
    mostrarSeccion('online');
  }
});
