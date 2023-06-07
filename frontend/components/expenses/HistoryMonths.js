import React, { useEffect } from 'react';
import Chart from 'chart.js/auto';

import { getExpensesForHistoryChart, getMonthsForHistoryChart } from '../../utils/utils';

const HistoryMonths = ({data}) => {

  useEffect(() => {
    
    const container = document.getElementById('history-months-chart').getContext('2d');
    const months_for_chart = getMonthsForHistoryChart(data.expenses)

    const chart = new Chart(container, {
      type: 'line',
      data: {
        labels: months_for_chart,
        datasets: [
          {
            label: 'Gastos Operacionales',
            data: getExpensesForHistoryChart(data.expenses.operational, months_for_chart),
            backgroundColor: '#d7f5eb',
            borderWidth: 3,
            borderColor: '#AEEBD8',
            borderRadius: 10,
            borderSkipped: false,
          },
          // {
          //   label: 'Oficinas Parlamentarias',
          //   data: getExpensesForHistoryChart(data.expenses.offices, months_for_chart),
          //   backgroundColor: '#afc1fa',
          //   borderWidth: 3,
          //   borderColor: '#9BABDE',
          //   borderRadius: 10,
          //   borderSkipped: false,
          // },
          {
            label: 'Personal de Apoyo',
            data: getExpensesForHistoryChart(data.expenses.staff, months_for_chart),
            backgroundColor: '#ded5f5',
            borderWidth: 3,
            borderColor: '#CBB5FF',
            borderRadius: 10,
            borderSkipped: false,
          },
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
          },
          title: {
            display: true,
            text: 'Historial 6 meses',
            font: {
              size: 24,
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
    });

    return () => chart.destroy();

  }, [])

  return (
    <>
      <div className='image chart-container-4'>
        <canvas id='history-months-chart'></canvas>
      </div>
      <div className='content'>
        <h3>Progresión de Gastos</h3>
        <p>
          Se presenta además la evolución de los gastos en los <strong>últimos 6 meses</strong><a href='#ref-6'><sup>6</sup></a>.
        </p>
      </div>
    </>
  )
}

export default HistoryMonths