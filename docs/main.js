const map = L.map('map').setView([41.38, 2.17], 13); // Posición inicial en Barcelona

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

const marker = L.marker([0, 0]).addTo(map);

async function fetchLatestLocation() {
  try {
    const response = await fetch('https://backend-tfg-qzd9.onrender.com/data');
    const data = await response.json();

    const lat = data.latitude;
    const lon = data.longitude;

    if (!isNaN(lat) && !isNaN(lon)) {
      marker.setLatLng([lat, lon]);
      map.setView([lat, lon], 16);
    }
  } catch (err) {
    console.error("Error al obtener datos del backend:", err);
  }
}

fetchLatestLocation();
setInterval(fetchLatestLocation, 30000);
