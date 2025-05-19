// server.js
const express = require('express');
const fetch = require('node-fetch');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3000;
const TTN_API_KEY = process.env.TTN_API_KEY;
const TTN_APP_ID = 'mkrgpslora'; // Cambia esto si tu app TTN tiene otro nombre

app.use(cors());

app.get('/data', async (req, res) => {
  const url = `https://eu1.cloud.thethings.network/api/v3/as/applications/${TTN_APP_ID}/packages/storage/uplink_message`;

  try {
    const response = await fetch(url, {
      headers: {
        Authorization: `Bearer ${TTN_API_KEY}`,
      },
    });

    if (!response.ok) {
      throw new Error(`TTN API error: ${response.status}`);
    }

    const data = await response.json();
    res.json(data);
  } catch (err) {
    console.error('Error al obtener datos de TTN:', err);
    res.status(500).json({ error: 'No se pudo acceder a TTN' });
  }
});

app.get('/', (req, res) => {
  res.send('Servidor TTN funcionando. Usa /data para obtener ubicación.');
});

app.listen(PORT, () => {
  console.log(`Servidor escuchando en puerto ${PORT}`);
});
