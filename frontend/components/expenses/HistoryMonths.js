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
            label: "Gastos Operacionales",
            data: getExpensesForHistoryChart(data.expenses.operational, months_for_chart),
            backgroundColor: '#AEEBD8',
            borderWidth: 2,
            borderRadius: 10,
            borderSkipped: false,
          },
          {
            label: "Oficinas Parlamentarias",
            data: getExpensesForHistoryChart(data.expenses.offices, months_for_chart),
            backgroundColor: '#9BABDE',
            borderWidth: 2,
            borderRadius: 10,
            borderSkipped: false,
          },
          {
            label: "Personal de Apoyo",
            data: getExpensesForHistoryChart(data.expenses.staff, months_for_chart),
            backgroundColor: '#CBB5FF',
            borderWidth: 2,
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
            text: 'Gastos',
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
      <div className='image add-padding'>
        <canvas id='history-months-chart'></canvas>
      </div>
      <div className="content">
        <h3>Progresión de Gastos</h3>
        <p>
          Se presenta además la evolución de los gastos en los <strong>últimos 6 meses</strong><a href='#ref-expenses'><sup>5</sup></a>
        </p>
      </div>
    </>
  )
}

export default HistoryMonths