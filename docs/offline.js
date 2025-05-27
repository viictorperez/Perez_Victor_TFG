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

    if (chart) chart.destroy();

    const ctx = document.getElementById('grafico').getContext('2d');
    chart = new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [
                {
                    label: 'Emisores',
                    data: puntos,
                    backgroundColor: 'rgba(0,123,255,0.7)'
                },
                {
                    label: 'Receptor',
                    data: [{ x: 0, y: 0 }],
                    backgroundColor: 'rgba(255,0,0,0.9)',
                    pointRadius: 8
                }
            ]
        },
        options: {
            scales: {
                x: { title: { display: true, text: 'Eje X' } },
                y: { title: { display: true, text: 'Eje Y' } }
            }
        }
    });
}
