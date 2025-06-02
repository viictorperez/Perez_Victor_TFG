let chart;
let datos = [];
let indiceActual = 0;

const PROFUNDIDAD_RECEPTOR = 100;
const RANGO_MAXIMO = 300; 

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
    const punto = calcularDireccion(az, el);
    puntosDireccion.push(punto);
    profundidades.push(punto.profundidad);
  } else if (isNumber(r)) {
    const punto = calcularPresencia(r);
    puntosPresencia.push(punto);
  }

  const minDepth = Math.min(...profundidades);
  const maxDepth = Math.max(...profundidades);

  if (chart) chart.destroy();

  const ctx = document.getElementById('grafico').getContext('2d');
  chart = new Chart(ctx, {
    type: 'scatter',
    data: {
      datasets: [
        {
          label: 'Posición exacta',
          data: puntosExactos.map(p => ({ x: p.x, y: p.y })),
          pointBackgroundColor: puntosExactos.map(p =>
            getColorForDepth(p.profundidad, minDepth, maxDepth)
          ),
          pointRadius: 6
        },
        {
          label: 'Dirección estimada',
          data: puntosDireccion.flatMap(p => [
            { x: p.x1, y: p.y1 },
            { x: p.x2, y: p.y2 }
          ]),
          borderColor: 'blue',
          borderWidth: 2,
          showLine: true,
          fill: false,
          pointRadius: 0
        },
        {
          label: 'Presencia (rango)',
          data: puntosPresencia.map(p => ({ x: 0, y: 0 })),
          backgroundColor: 'red',
          pointRadius: puntosPresencia.map(p => p.rango / 5)
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
  const profundidad = PROFUNDIDAD_RECEPTOR + z;
  return { x, y, profundidad };
}

function calcularDireccion(az, el) {
  const r = RANGO_MAXIMO;
  const azRad = az * Math.PI / 180;
  const elRad = el * Math.PI / 180;
  const x = r * Math.cos(elRad) * Math.sin(azRad);
  const y = r * Math.cos(elRad) * Math.cos(azRad);
  const z = r * Math.sin(elRad);
  const profundidad = PROFUNDIDAD_RECEPTOR + z;
  return {
    x1: 0,
    y1: 0,
    x2: x,
    y2: y,
    profundidad
  };
}


function calcularPresencia(r) {
  return { rango: r };
}

function getColorForDepth(depth, min, max) {
  const ratio = (depth - min) / (max - min);
  const blue = Math.round(255 - ratio * 200);
  return `rgb(0,0,${blue})`;
}

function isNumber(n) {
  return typeof n === 'number' && !isNaN(n);
}
