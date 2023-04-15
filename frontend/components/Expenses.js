import React, { useEffect, useState } from 'react';
import Chart from 'chart.js/auto';

import styles from '../styles/home/Expenses.module.css';

const formatAmount = (amount) => {
  return '$'+amount.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

const getMonthsForHistoryChart = (expenses) => {
  const operational_months = expenses.operational.map((expense) => expense.month).reverse()
  const offices_months = expenses.offices.map((expense) => expense.month).reverse()
  const staff_months = expenses.staff.map((expense) => expense.month).reverse()
  const months = [...new Set([...operational_months,...offices_months, ...staff_months])]
  return months
}

const getExpensesForHistoryChart = (expenses, months) => {
  let expenses_by_month = {}
  for (let expense of expenses) {
    expenses_by_month[expense.month] = expense.total
  }
  return months.map((month) => expenses_by_month[month] || undefined)
}


const Expenses = ({deputyInfo}) => {

  const show_month = deputyInfo.expenses.operational[0].month

  const opExp_month = deputyInfo.expenses.operational.filter(expenses => expenses.month == show_month);
  const show_operational = opExp_month.length > 0 ? opExp_month[0].total : 0;
  const mean_operational = opExp_month.length > 0 ? opExp_month[0].mean : 0;

  const ofExp_month = deputyInfo.expenses.offices.filter(expenses => expenses.month == show_month);
  const show_offices = ofExp_month.length > 0 ? ofExp_month[0].total : 0;
  const mean_offices = ofExp_month.length > 0 ? ofExp_month[0].mean : 0;
  
  const stExp_month = deputyInfo.expenses.staff.filter(expenses => expenses.month == show_month);
  const show_staff = stExp_month.length > 0 ? stExp_month[0].total : 0;
  const mean_staff = stExp_month.length > 0 ? stExp_month[0].mean : 0;

  const show_total = formatAmount(show_operational + show_offices + show_staff);
  const size = window.innerWidth < 600 ? 300 : 400;
  
  const months_for_chart = getMonthsForHistoryChart(deputyInfo.expenses)

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

    const mainExpensesContainer = document.getElementById('mainExpensesChart').getContext('2d');
    const operationalExpensesContainer = document.getElementById('operationalExpensesChart').getContext('2d');
    const historyExpensesContainer = document.getElementById('historyExpensesChart').getContext('2d');

    const charts = [
      new Chart(mainExpensesContainer, {
        type: 'bar',
        data: {
          labels: ["Gastos Operacionales", "Oficinas Parlamentarias", "Personal de Apoyo"],
          datasets: [
            {
              label: "Promedio Diputadxs",
              backgroundColor: ["#cccccc", "#cccccc", "#cccccc"],
              data: [ mean_operational, mean_offices, mean_staff ],
              borderWidth: 2,
              borderRadius: 10,
              borderSkipped: false,
              stack: 'combined',
              type: 'line',
              cubicInterpolationMode: 'monotone',
              tension: 0.4
            },
            {
              label: "Gastos Diputadx",
              backgroundColor: ["#BA5DE8", "#5961FF", "#02B4F5"],
              data: [ show_operational, show_offices, show_staff ],
              borderWidth: 2,
              borderRadius: 10,
              borderSkipped: false,
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'top',
              display: false,
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
          labels: op_keys,
          datasets: [
            {
              label: "Promedio Diputadxs",
              data: op_keys.map((op_key) => deputyInfo.expenses.operational[0][op_key]['mean']),
              backgroundColor: ['#ff6961', '#ffb480', '#f8f38d', '#42d6a4', '#08cad1', '#59adf6', '#9d94ff', '#c780e8'],
              borderWidth: 2,
              borderRadius: 10,
              borderSkipped: false,
              borderColor: '#ff0000',
              stack: 'combined',
              type: 'line',
              cubicInterpolationMode: 'monotone',
              tension: 0.4
            },
            {
              label: "Gastos Diputadx",
              data: op_keys.map((op_key) => deputyInfo.expenses.operational[0][op_key]['amount']),
              backgroundColor: ['#ff6961', '#ffb480', '#f8f38d', '#42d6a4', '#08cad1', '#59adf6', '#9d94ff', '#c780e8'],
              borderWidth: 2,
              borderRadius: 10,
              borderSkipped: false,
            },
          ]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'top',
              display: false,
            },
            title: {
              display: true,
              text: 'Distribución de Gastos Operacionales ('+formatAmount(show_operational)+')',
              font: {
                size: 18,
              }
            },
          },
        }
      }),
      new Chart(historyExpensesContainer, {
        type: 'line',
        data: {
          labels: months_for_chart,
          datasets: [
            {
              label: "Gastos Operacionales",
              data: getExpensesForHistoryChart(deputyInfo.expenses.operational, months_for_chart),
              backgroundColor: '#ff6961',
              borderWidth: 2,
              borderRadius: 10,
              borderSkipped: false,
            },
            {
              label: "Arriendo de Oficinas",
              data: getExpensesForHistoryChart(deputyInfo.expenses.offices, months_for_chart),
              backgroundColor: '#ffb480',
              borderWidth: 2,
              borderRadius: 10,
              borderSkipped: false,
            },
            {
              label: "Personal de Apoyo",
              data: getExpensesForHistoryChart(deputyInfo.expenses.staff, months_for_chart),
              backgroundColor: '#42d6a4',
              borderWidth: 2,
              borderRadius: 10,
              borderSkipped: false,
            },
          ]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'bottom',
            },
            title: {
              display: true,
              text: 'Historial de Gastos',
              font: {
                size: 18,
              }
            },
          }
        }
      })
    ];

    return () => charts.map(chart => chart.destroy());
  
  }, [
    deputyInfo,
    months_for_chart, 
    show_operational, 
    show_offices, 
    show_staff, 
    show_month
  ]);


  return (
    <div className='container'>
      <header>
        <h2>Gastos</h2>
        <p>
          El último mes donde existe un registro completo de los gastos { deputyInfo.sex == 0 ? 'de la' : 'del' }
          {' '} diputad{deputyInfo.termination} <strong>{ deputyInfo.first_name } { deputyInfo.first_surname }</strong> corresponde a
          {' '} <strong>{deputyInfo.expenses.operational[0].month} de { deputyInfo.expenses.operational[0].year }</strong>,
          {' '} destinando un total de <strong>{ show_total }</strong><a href='#op-expenses'><sup>2,3,4</sup></a> entre gastos operacionales, 
          {' '} de oficina y personal de apoyo. En particular, se distribuyen de la siguiente manera:
        </p>
      </header>
      <div className={styles.chartContainer}>
        <div id='mainExpensesContainer'>
          <canvas id='mainExpensesChart' width={size*0.8} height={size}></canvas>
        </div>
        <div id='operationalExpensesContainer'>
          <canvas id='operationalExpensesChart' height={size*1.5} width={size*1.2}></canvas>
        </div>
      </div>
      <div className={styles.expensesHistoryIntroduction}>
        <p>
          Se presenta además la evolución de los gastos en los <strong>últimos 6 meses</strong><a href='#ref-expenses'><sup>5</sup></a>:
        </p>
      </div>
      <div className={styles.chartContainer}>
        <div id='historyExpensesContainer'>
          <canvas id='historyExpensesChart' height={size} width={size}></canvas>
        </div>
      </div>
    </div>
  )
}

export default Expenses