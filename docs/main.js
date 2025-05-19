// main.js
const map = L.map('map').setView([41.38, 2.17], 13); // Barcelona por defecto

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

const marker = L.marker([0, 0]).addTo(map);

async function fetchLatestLocation() {
  try {
    const response = await fetch('https://YOUR-RENDER-URL.onrender.com/data');
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
    console.error('Error obteniendo datos de ubicación:', err);
  }
}

fetchLatestLocation();
setInterval(fetchLatestLocation, 30000);
