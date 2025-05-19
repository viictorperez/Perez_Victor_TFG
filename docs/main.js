// main.js

const map = L.map('map').setView([41.38, 2.17], 13); // Posición inicial en Barcelona

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

const marker = L.marker([0, 0]).addTo(map);

async function fetchLatestLocation() {
  try {
    const response = await fetch('https://backend-tfg-qzd9.onrender.com'); 
    const data = await response.json();

    const last = data[data.length - 1];
    const gps = last.uplink_message.decoded_payload;

    if (gps && gps.latitude && gps.longitude) {
      const lat = gps.latitude;
      const lon = gps.longitude;
      marker.setLatLng([lat, lon]);
      map.setView([lat, lon], 16);
    }
  } catch (err) {
    console.error('Error al obtener datos de TTN:', err);
  }
}

// Ejecutar al cargar y luego cada 30 segundos
fetchLatestLocation();
setInterval(fetchLatestLocation, 30000);
