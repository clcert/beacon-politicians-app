import React, { useEffect } from 'react';
import Chart from 'chart.js/auto';

import styles from '../styles/home/Attendance.module.css';

const Attendance = ({deputyInfo}) => {

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
          <canvas id='attendanceChart' width='500' height='auto'></canvas>
        </div>
      </div>
    </div>
  )
}

export default Attendance