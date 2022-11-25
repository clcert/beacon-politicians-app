import React, { useEffect } from 'react';
import Chart from 'chart.js/auto';

import styles from '../styles/home/Expenses.module.css';

const obtainLastMonth = (expenses) => {
  return expenses[expenses.length - 1].month;
}

const totalOperationalExpensesMonth = (expenses) => {
  let total = 0;
  for (const [key, amount] of Object.entries(expenses)) {
    if ( key != 'month' ) {
      total += amount;
    }
  }
  return total;
}

const totalOfficesExpensesMonth = (offices) => {
  let total = 0;
  for (let office of offices) {
    total += office.amount;
  }
  return total;
}


const formatAmount = (amount) => {
  return '$'+amount.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}


const Expenses = ({deputyInfo}) => {

  const last_operational_month = obtainLastMonth(deputyInfo.expenses.operational);
  const total_operational_month = formatAmount(
    totalOperationalExpensesMonth(deputyInfo.expenses.operational[deputyInfo.expenses.operational.length - 1])
  );
  const last_offices_month = obtainLastMonth(deputyInfo.expenses.offices);
  const total_offices_month = formatAmount(
    totalOfficesExpensesMonth(deputyInfo.expenses.offices[deputyInfo.expenses.offices.length - 1].offices)
  );

  useEffect(() => {
    var ctx = document.getElementById('expensesChart').getContext('2d');
    var att = [
      deputyInfo.attendance.attended, 
      deputyInfo.attendance.justified, 
      deputyInfo.attendance.unjustified
    ];
    var myChart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: ["Días Asistidos", "Días no asistidos justificados", "Días no asistidos no justificados"],
        datasets: [{
          label: "Expenses",
          backgroundColor: ["#3cba9f", "#3e95cd", "#FF0000"],
          data: att,
        }]
      },
      options: {
        title: {
          display: true,
          text: 'Asistencia'
        }
      }
    });

    return () => myChart.destroy();
  
  }, [])


  return (
    <div className='container'>
      <header>
        <h2>Gastos</h2>
        <p>
          El último mes con registro de gastos operacionales corresponde a <strong>{last_operational_month}</strong>,
          &nbsp;donde { deputyInfo.sex == 0 ? 'la' : 'el' } diputad{deputyInfo.termination}
          &nbsp;<strong>{ deputyInfo.first_name } { deputyInfo.first_surname }</strong> destinó <strong>{ total_operational_month }</strong>
          &nbsp;para dicho fin. Respecto a los gastos de oficina, el último mes con registro corresponde a <strong>{last_offices_month}</strong>,
          &nbsp;incurriendo en un gasto de <strong>{ total_offices_month }</strong>.
        </p>
      </header>
      <div className={styles.chartContainer}>
        <div id='graphicContainer'>
          <canvas id='expensesChart' width='400' height='auto'></canvas>
        </div>
      </div>
    </div>
  )
}

export default Expenses