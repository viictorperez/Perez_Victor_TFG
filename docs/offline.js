let chart;

document.getElementById('csvFile').addEventListener('change', function(evt) {
    Papa.parse(evt.target.files[0], {
        header: true,
        dynamicTyping: true,
        complete: function(resultados) {
            crearGrafico(resultados.data);
        }
    });
});

function crearGrafico(datos) {
    const puntos = datos.map(fila => {
        if (fila.azimut !== undefined && fila.angulo !== undefined && fila.rango !== undefined) {
            let anguloRad = fila.angulo * Math.PI / 180;
            return {
                x: fila.rango * Math.cos(anguloRad),
                y: fila.rango * Math.sin(anguloRad)
            };
        } else if (fila.x !== undefined && fila.y !== undefined) {
            return { x: fila.x, y: fila.y };
        }
    }).filter(p => p);

    puntos.push({ x: 0, y: 0 }); // asegurar que 0,0 está incluido para centrado automático

    const xs = puntos.map(p => p.x);
    const ys = puntos.map(p => p.y);
    const margen = 20;

    const minX = Math.min(...xs, 0) - margen;
    const maxX = Math.max(...xs, 0) + margen;
    const minY = Math.min(...ys, 0) - margen;
    const maxY = Math.max(...ys, 0) + margen;

    if (chart) chart.destroy();

    const ctx = document.getElementById('grafico').getContext('2d');
    chart = new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [
                {
                    label: 'Emisores',
                    data: puntos.filter(p => p.x !== 0 || p.y !== 0),
                    backgroundColor: 'rgba(0,123,255,0.7)'
                },
                {
                    label: 'Receptor (0,0)',
                    data: [{ x: 0, y: 0 }],
                    backgroundColor: 'rgba(255,0,0,0.9)',
                    pointRadius: 7
                }
            ]
        },
        options: {
            animation: false,
            scales: {
                x: {
                    min: minX,
                    max: maxX,
                    title: { display: true, text: 'X' }
                },
                y: {
                    min: minY,
                    max: maxY,
                    title: { display: true, text: 'Y' }
                }
            },
            plugins: {
                legend: {
                    position: 'top',
                    labels: { boxWidth: 12 }
                }
            }
        }
    });
}
