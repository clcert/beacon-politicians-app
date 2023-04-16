import React, { useEffect } from 'react';
import Chart from 'chart.js/auto';

import { formatAmount } from '../../utils/utils';

const ExpensesSummary = ({data}) => {

  const show_month = data.expenses.operational[0].month
  const show_year = data.expenses.operational[0].year

  const opExp_month = data.expenses.operational.filter(expenses => expenses.month == show_month);
  const ofExp_month = data.expenses.offices.filter(expenses => expenses.month == show_month);
  const stExp_month = data.expenses.staff.filter(expenses => expenses.month == show_month);


  const chart_labels = ["Gastos Operacionales", "Oficinas Parlamentarias", "Personal de Apoyo"];
  const chart_colors = ["#AEEBD8", "#9BABDE", "#CBB5FF"];
  const chart_data = [
    opExp_month.length > 0 ? opExp_month[0].total : 0,
    ofExp_month.length > 0 ? ofExp_month[0].total : 0,
    stExp_month.length > 0 ? stExp_month[0].total : 0,
  ];
  const chart_mean = [
    opExp_month.length > 0 ? opExp_month[0].mean : 0,
    ofExp_month.length > 0 ? ofExp_month[0].mean : 0,
    stExp_month.length > 0 ? stExp_month[0].mean : 0,
  ]

  const total_amount = formatAmount(chart_data.reduce((a, b) => a + b, 0));

  useEffect(() => {
    const container = document.getElementById('summary-expenses-chart').getContext('2d');
    const chart = new Chart(container, {
      type: 'bar',
      data: {
        labels: chart_labels,
        datasets: [
          {
            label: "Promedio Diputadxs",
            backgroundColor: chart_colors,
            data: chart_mean,
            borderWidth: 2,
            borderRadius: 10,
            borderSkipped: false,
            borderColor: '#AAAAAA',
            stack: 'combined',
            type: 'line',
            cubicInterpolationMode: 'monotone',
            tension: 0.4
          },
          {
            label: "Gastos Diputadx",
            backgroundColor: chart_colors,
            data: chart_data,
            barPercentage: 0.75,
            borderWidth: 2,
            borderRadius: 10,
            borderSkipped: false,
          },
        ],
      },
      options: {
        maintainAspectRatio: false,
        responsive: true,
        plugins: {
          legend: {
            position: 'top',
            display: false,
          },
          title: {
            display: true,
            text: `Gastos de ${show_month} de ${show_year}`,
            font: {
              size: 24,
            },
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
      },
    });

    return () => chart.destroy()
  }, [])


  return (
    <>
      <div className='image add-padding'>
        <canvas id='summary-expenses-chart'></canvas>
      </div>
      <div className="content">
        <h3>Resumen de Gastos</h3>
        <p>
          El último mes donde existe un registro completo de los gastos { data.sex == 0 ? 'de la' : 'del' }
          {' '} diputad{data.termination} <strong>{ data.first_name } { data.first_surname }</strong> corresponde a
          {' '} <strong>{data.expenses.operational[0].month} de { data.expenses.operational[0].year }</strong>,
          {' '} destinando un total de <strong>{ total_amount }</strong><a href='#op-expenses'><sup>2,3,4</sup></a> entre gastos operacionales, 
          {' '} de oficina y personal de apoyo.
        </p>
      </div>
    </>
  )
}

export default ExpensesSummary