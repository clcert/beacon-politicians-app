import React, { useEffect } from 'react';
import Chart from 'chart.js/auto';

import { formatAmount } from '../../utils/utils';

const OperationalDistribuition = ({data}) => {

  const show_month = data.expenses.operational[0].month
  const opExp_month = data.expenses.operational.filter(expenses => expenses.month == show_month);
  const show_operational = opExp_month.length > 0 ? opExp_month[0].total : 0;

  useEffect(() => {
    const op_keys = [
      'Telefonía',
      'Traslación',
      'Difusión',
      'Correspondencia',
      'Relacionados a Oficina Parlamentaria',
      'Web y Almacenamiento',
      'Actividades destinadas a la interacción con la comunidad',
      'Otros',
    ];

    const short_keys = [
      'Telefonía',
      'Traslación',
      'Difusión',
      'Correspondencia',
      'Oficina Parlamentaria',
      'Web y Almacenamiento',
      'Interacción Comunitaria',
      'Otros',
    ];

    const container = document.getElementById('operational-distribuition-chart').getContext('2d');
    const chart_mean = op_keys.map((op_key) => data.expenses.operational[0][op_key]['mean']);
    const chart_data = op_keys.map((op_key) => data.expenses.operational[0][op_key]['amount']);
    const chart_colors = ['#ff6961', '#ffb480', '#f8f38d', '#42d6a4', '#08cad1', '#59adf6', '#9d94ff', '#c780e8'];

    const chart = new Chart(container, {
      type: 'bar',
      data: {
        labels: short_keys,
        datasets: [
          {
            label: 'Promedio Diputadxs',
            data: chart_mean,
            backgroundColor: '#2F58CD',
            borderWidth: 2,
            borderRadius: 10,
            borderSkipped: false,
            borderColor: '#2F58CD',
            stack: 'combined',
            type: 'line',
            cubicInterpolationMode: 'monotone',
            tension: 0.4
          },
          {
            label: `Gastos Diputad${data.termination}`,
            data: chart_data,
            backgroundColor: chart_colors,
            borderColor: '#fff',
            borderWidth: 2,
            borderRadius: 10,
            borderSkipped: false,
          },
        ]
      },
      options: {
        maintainAspectRatio: false,
        responsive: true,
        plugins: {
          legend: {
            position: 'top',
            display: true,
          },
          title: {
            display: true,
            text: 'Gastos Operacionales ('+formatAmount(show_operational)+')',
            font: {
              size: 20,
            }
          },
        },
        scales: {
          y: {
            ticks: {
              font: {
                size: 14,
              }
            }
          },
          x: {
            ticks: {
              font: {
                size: 14,
              }
            }
          }
        }
      }
    })

    return () => chart.destroy()
  }, [])

  return (
    <>
      <div className='image chart-container-3'>
        <canvas id='operational-distribuition-chart'></canvas>
      </div>
      <div className='content'>
        <h3>Distribución de Gastos Operacionales</h3>
        <p>
          Los gastos operacionales del mes indicado se distribuyen según
          indica el gráfico adjunto.
        </p>
      </div>
    </>
  )
}

export default OperationalDistribuition