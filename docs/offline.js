let chart;
let datos = [];
let indiceActual = 0;

Chart.register({
  id: 'equalScale',
  afterLayout(chart) {
    const x = chart.scales.x;
    const y = chart.scales.y;

    if (!x || !y || !chart.chartArea) return;

    const xRange = x.max - x.min;
    const yRange = y.max - y.min;

    const pixelRatioX = chart.chartArea.width / xRange;
    const pixelRatioY = chart.chartArea.height / yRange;

    if (Math.abs(pixelRatioX - pixelRatioY) < 1e-2) return;

    if (pixelRatioX > pixelRatioY) {
      const center = (x.max + x.min) / 2;
      const newRange = chart.chartArea.width / pixelRatioY;
      x.options.min = center - newRange / 2;
      x.options.max = center + newRange / 2;
    } else {
      const center = (y.max + y.min) / 2;
      const newRange = chart.chartArea.height / pixelRatioX;
      y.options.min = center - newRange / 2;
      y.options.max = center + newRange / 2;
    }

    chart.update('none');
  }
});

const PROFUNDIDAD_RECEPTOR = 300;
const RANGO_MAXIMO = 200; 

document.getElementById('csvFile').addEventListener('change', function(evt) {
  Papa.parse(evt.target.files[0], {
    header: true,
    dynamicTyping: (field) => field !== 'timestamp',
    complete: function(resultados) {
      datos = resultados.data.filter(f => f.id !== undefined); // ignora líneas vacías
      indiceActual = 0;
      mostrarFila(indiceActual);
    }
  });
});

document.getElementById('prevBtn').addEventListener('click', () => {
  if (indiceActual > 0) {
    indiceActual--;
    mostrarFila(indiceActual);
  }
});

document.getElementById('nextBtn').addEventListener('click', () => {
  if (indiceActual < datos.length - 1) {
    indiceActual++;
    mostrarFila(indiceActual);
  }
});

function mostrarFila(i) {
  const fila = datos[i];
  const puntosExactos = [];
  const puntosDireccion = [];
  const puntosPresencia = [];
  let profundidades = [];

  const az = fila.azimut;
  const el = fila.elevacion;
  const r = fila.rango;

  if (isNumber(az) && isNumber(el) && isNumber(r)) {
    const punto = calcularPosicionExacta(az, el, r);
    puntosExactos.push(punto);
    profundidades.push(punto.profundidad);
  } else if (isNumber(az) && isNumber(el)) {
    const puntos = calcularDireccion(az, el);
    puntosDireccion.push(...puntos);
    profundidades.push(...puntos.map(p => p.profundidad));
  } else if (isNumber(r)) {
    const punto = calcularPresencia(r);
    puntosPresencia.push(punto);
  }

  const minDepth = PROFUNDIDAD_RECEPTOR - RANGO_MAXIMO;
  const maxDepth = PROFUNDIDAD_RECEPTOR + RANGO_MAXIMO;

  if (chart) chart.destroy();

  const ctx = document.getElementById('grafico').getContext('2d');

  chart = new Chart(ctx, {
    type: 'scatter',
    data: {
      datasets: [
        {
          label: 'Posición exacta',
          data: puntosExactos.map(p => ({ x: p.x, y: p.y, profundidad: p.profundidad })),
          pointBackgroundColor: puntosExactos.map(p =>
            getColorForDepth(p.profundidad, minDepth, maxDepth)
          ),
          pointRadius: 6
        },
        {
          label: 'Dirección estimada',
          data: puntosDireccion.map(p => ({ x: p.x, y: p.y, profundidad: p.profundidad })),
          pointBackgroundColor: puntosDireccion.map(p =>
            getColorForDepth(p.profundidad, minDepth, maxDepth)
          ),
          pointRadius: 3,
          showLine: false
        },
        {
          label: 'Presencia (rango)',
          data: puntosPresencia.map(p => ({ x: 0, y: 0, rango: p.rango })),
          backgroundColor: 'red',
          pointRadius: puntosPresencia.map(p => p.rango)
        },
        {
          label: 'Receptor (0,0)',
          data: [{ x: 0, y: 0 }],
          backgroundColor: 'black',
          pointRadius: 8
        }
      ]
    },
    options: {  
      animation: false,
      maintainAspectRatio: false,
      layout: {
        padding: 100
      },
      scales: {
        x: {
          min: -RANGO_MAXIMO,
          max: RANGO_MAXIMO,
          title: { display: true, text: 'X (m)' }
        },
        y: {
          min: -RANGO_MAXIMO,
          max: RANGO_MAXIMO,
          title: { display: true, text: 'Y (m)' }
        }
      },
      plugins: {
        tooltip: {
          callbacks: {
            label: function(context) {
              const datasetLabel = context.dataset.label;
              const p = context.raw;
            
              if (datasetLabel === 'Receptor (0,0)') {
                return ''; // No mostrar nada
              }
            
              if (datasetLabel === 'Presencia (rango)') {
                return `Rango: ${p.rango?.toFixed(1) ?? '?'}`;
              }
            
              return `(${p.x.toFixed(1)}, ${p.y.toFixed(1)}, ${p.profundidad?.toFixed(1) ?? '?'})`;
            }
          }
        },
        legend: {
          position: 'right',
          labels: { boxWidth: 12 }
        }
      }
    }
  });


  // Actualizar leyenda y estado
  document.getElementById('infoFila').innerText = `Hora: ${fila.timestamp || 'desconocida'}`;

  if (profundidades.length > 0) {
    document.getElementById('profundidad-min').innerText = minDepth.toFixed(1) + ' m';
    document.getElementById('profundidad-max').innerText = maxDepth.toFixed(1) + ' m';
  } else {
    document.getElementById('profundidad-min').innerText = '-';
    document.getElementById('profundidad-max').innerText = '-';
  }
}

function calcularPosicionExacta(az, el, r) {
  const azRad = az * Math.PI / 180;
  const elRad = el * Math.PI / 180;
  const x = r * Math.cos(elRad) * Math.sin(azRad);
  const y = r * Math.cos(elRad) * Math.cos(azRad);
  const z = r * Math.sin(elRad);
  const profundidad = PROFUNDIDAD_RECEPTOR - z;  
  return { x, y, profundidad };
}

function calcularDireccion(az, el, segmentos = 20) {
  const azRad = az * Math.PI / 180;
  const elRad = el * Math.PI / 180;
  const puntos = [];

  for (let i = 1; i <= segmentos; i++) {
    const r = (RANGO_MAXIMO * i) / segmentos;
    const x = r * Math.cos(elRad) * Math.sin(azRad);
    const y = r * Math.cos(elRad) * Math.cos(azRad);
    const z = r * Math.sin(elRad);
    const profundidad = PROFUNDIDAD_RECEPTOR - z; 
    puntos.push({ x, y, profundidad });
  }

  return puntos;
}

function calcularPresencia(r) {
  return { rango: r };
}

function getColorForDepth(depth, min, max) {
  const ratio = (depth - min) / (max - min);
  const r = Math.min(Math.max(ratio, 0), 1);
  const hue = (1 - r) * 240;
  return `hsl(${hue}, 100%, 50%)`;
}

function isNumber(n) {
  return typeof n === 'number' && !isNaN(n);
}
