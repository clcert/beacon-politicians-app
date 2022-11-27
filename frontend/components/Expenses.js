import React, { useEffect } from 'react';
import Chart from 'chart.js/auto';

import styles from '../styles/home/Expenses.module.css';

const formatAmount = (amount) => {
  return '$'+amount.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}


const Expenses = ({deputyInfo}) => {

  const show_month = deputyInfo.expenses.operational[0].month

  const show_operational = deputyInfo.expenses.operational[0].total;
  const show_offices = deputyInfo.expenses.offices.filter(expenses => expenses.month == show_month)[0].total;
  const show_staff = deputyInfo.expenses.staff.filter(expenses => expenses.month == show_month)[0].total;

  const show_total = formatAmount(show_operational + show_offices + show_staff);

  const op_keys = [
    'Telefonía',
    'Traslación',
    'Difusión',
    'Actividades destinadas a la interacción con la comunidad',
    'Correspondencia',
    'Relacionados a Oficina Parlamentaria',
    'Web y Almacenamiento',
    'Otros',
  ]
  
  Object.keys(deputyInfo.expenses.operational[0]).filter(key => key != 'month' && key != 'total' && key != 'year');

  useEffect(() => {
    const mainExpensesContainer = document.getElementById('mainExpensesChart').getContext('2d');
    const operationalExpensesContainer = document.getElementById('operationalExpensesChart').getContext('2d');

    const charts = [
      new Chart(mainExpensesContainer, {
        type: 'doughnut',
        data: {
          labels: ["Gastos Operacionales", "Oficinas Parlamentarias", "Personal de Apoyo"],
          datasets: [{
            label: "Expenses",
            backgroundColor: ["#BA5DE8", "#5961FF", "#02B4F5"],
            data: [ show_operational, show_offices, show_staff ],
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'bottom',
            },
            title: {
              display: true,
              text: 'Gastos de ' + show_month,
              font: {
                size: 18,
              }
            }
          }
        }
      }),
      new Chart(operationalExpensesContainer, {
        type: 'bar',
        data: {
          labels: ['Telefonía','Traslación','Difusión','Interacción con Comunidad','Correspondencia','Oficina Parlamentaria','Web y Almacenamiento','Otros'],
          datasets: [{
            label: "Expenses",
            data: op_keys.map((op_key) => deputyInfo.expenses.operational[0][op_key]),
            backgroundColor: ['#ff6961', '#ffb480', '#f8f38d', '#42d6a4', '#08cad1', '#59adf6', '#9d94ff', '#c780e8'],
            borderWidth: 2,
            borderRadius: 10,
            borderSkipped: false,
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'bottom',
              display: false,
            },
            title: {
              display: true,
              text: 'Gastos Operacionales ('+formatAmount(show_operational)+')',
              font: {
                size: 18,
              }
            },
          }
        }
      })
    ];

    return () => charts.map(chart => chart.destroy());
  
  }, [])


  return (
    <div className='container'>
      <header>
        <h2>Gastos</h2>
        <p>
          El último mes donde existe un registro completo de los gastos { deputyInfo.sex == 0 ? 'de la' : 'del' }
          {' '} diputad{deputyInfo.termination} <strong>{ deputyInfo.first_name } { deputyInfo.first_surname }</strong> corresponde a
          {' '} <strong>{deputyInfo.expenses.operational[0].month} de { deputyInfo.expenses.operational[0].year }</strong>,
          {' '} destinando un total de <strong>{ show_total }</strong> entre gastos operacionales, de oficina y personal de apoyo. En particular,
          se distribuyen de la siguiente manera:
        </p>
      </header>
      <div className={styles.chartContainer}>
        <div id='mainExpensesContainer'>
          <canvas id='mainExpensesChart' width='400' height='auto'></canvas>
        </div>
        <div id='operationalExpensesContainer'>
          <canvas id='operationalExpensesChart' height='400' width='400'></canvas>
        </div>
      </div>
    </div>
  )
}

export default Expenses