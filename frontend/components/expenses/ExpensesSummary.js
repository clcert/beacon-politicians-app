import React, { useEffect } from 'react';
import Chart from 'chart.js/auto';

import { formatAmount } from '../../utils/utils';

const ExpensesSummary = ({data}) => {

  const show_month = data.expenses.operational[0].month
  const show_year = data.expenses.operational[0].year

  const opExp_month = data.expenses.operational.filter(expenses => expenses.month == show_month);
  const ofExp_month = data.expenses.offices.filter(expenses => expenses.month == show_month);
  const stExp_month = data.expenses.staff.filter(expenses => expenses.month == show_month);

  const parlamentary_diet = 7012338;


  const chart_labels = [ 'Dieta Parlamentaria', 'Gastos Operacionales', 'Oficinas Parlamentarias', 'Personal de Apoyo'];
  // const chart_colors = ['#AA77FF', '#62CDFF', '#FFB84C'];
  const chart_data = [
    parlamentary_diet,
    opExp_month.length > 0 ? opExp_month[0].total : 0,
    ofExp_month.length > 0 ? ofExp_month[0].total : 0,
    stExp_month.length > 0 ? stExp_month[0].total : 0,
  ];
  const chart_mean = [
    parlamentary_diet,
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
            label: 'Promedio Diputadxs',
            backgroundColor: '#2F58CD',
            data: chart_mean,
            borderWidth: 2,
            borderRadius: 10,
            borderSkipped: false,
            stack: 'combined',
            type: 'line',
            showLine: false,
            pointStyle: 'circle',
          },
          {
            label: `Gastos Diputad${data.termination}`,
            backgroundColor: '#FFB84C',
            data: chart_data,
            barPercentage: 0.6,
            borderWidth: 2,
            borderRadius: 10,
            borderColor: '#fff',
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
            display: true,
          },
          title: {
            display: true,
            text: `Gastos de ${show_month} de ${show_year}`,
            font: {
              size: 20,
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
      <div className='image chart-container-2'>
        <canvas id='summary-expenses-chart'></canvas>
      </div>
      <div className='content'>
        <h3>Resumen</h3>
        <p>
          El último mes donde existe un registro completo de los gastos { data.sex == 0 ? 'de la' : 'del' }
          {' '} diputad{data.termination} <strong>{ data.first_name } { data.first_surname }</strong> corresponde a
          {' '} <strong>{data.expenses.operational[0].month} de { data.expenses.operational[0].year }</strong>.
          {' '} Sumando la dieta parlamentaria <sup><a href='#ref-2'>2</a></sup> con las asignaciones para gastos
          {' '} operacionales<sup><a href='#ref-3'>3</a></sup>, oficinas parlamentarias<sup><a href='#ref-4'>4</a></sup>
          {' '} y personal de apoyo<sup><a href='#ref-5'>5</a></sup>, se obtiene un total de <strong>{ total_amount }</strong>.
        </p>
      </div>
    </>
  )
}

export default ExpensesSummary