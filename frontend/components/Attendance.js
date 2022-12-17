import React, { useEffect } from 'react';
import Chart from 'chart.js/auto';

import styles from '../styles/home/Attendance.module.css';

const Attendance = ({deputyInfo}) => {

  const size = window.innerWidth < 600 ? 300 : 400;

  useEffect(() => {
    var ctx = document.getElementById("attendanceChart").getContext('2d');
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
          label: "Attendance",
          backgroundColor: ["#3cba9f", "#3e95cd", "#FF0000"],
          data: att,
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
            text: 'Asistencia',
            font: {
              size: 18,
            }
          }
        }
      }
    });

    return () => myChart.destroy();
  
  }, [deputyInfo])

  return (
    <div className='container'>
      <header>
        <h2>Asistencia</h2>
        <p>
          A la fecha de consulta, ha asistido a <strong>{ deputyInfo.attendance.attended } sesiones de cámara</strong>, 
          de un total de { deputyInfo.attendance.total } sesiones, obteniendo así un <strong>{ deputyInfo.attendance.percentage }% 
          de asistencia justificada</strong>. Considerando las inasistencias justificadas y las no justificadas
          <sup><a id='text-attendance' href='#ref-attendance'>1</a></sup>, se puede apreciar el siguiente gráfico:
        </p>
      </header>
      <div className={styles.chartContainer}>
        <div id='graphicContainer'>
          <canvas id='attendanceChart' width={size} height={size}></canvas>
        </div>
      </div>
    </div>
  )
}

export default Attendance