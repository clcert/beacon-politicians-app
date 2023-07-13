import React, { useEffect } from 'react';
import Chart from 'chart.js/auto';

const DeputyAttendance = ({attendance, gender}) => {

  const depPronoun = gender === 'MALE' ? 'el diputado' : 'la diputada';

  useEffect(() => {
    var container = document.getElementById('attendances-chart').getContext('2d');
    var attendances_data = [
      attendance.attended, 
      attendance.justified_absent, 
      attendance.unjustified_absent,
    ];
    var myChart = new Chart(container, {
      type: 'doughnut',
      data: {
        labels: ["Días Asistidos", "Días no asistidos justificados", "Días no asistidos no justificados"],
        datasets: [{
          label: "Attendance",
          backgroundColor: ["#3cba9f", "#3e95cd", "#FF0000"],
          data: attendances_data,
        }]
      },
      options: {
        maintainAspectRatio: false,
        responsive: true,
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              font: {
                size: 14,
              }
            }
          },
          title: {
            display: true,
            text: 'Asistencia',
            font: {
              size: 20,
            }
          }
        }
      }
    });

    return () => myChart.destroy();
  
  }, [attendance])

  return (
    <>
      <div className='image chart-container-1'>
        <canvas id='attendances-chart' height='100%'></canvas>
      </div>
      <div className="content">
        <p>
          A la fecha, { depPronoun } ha asistido a <strong>{ attendance.attended } sesiones de cámara</strong>, 
          de un total de { attendance.total } sesiones dentro de la legislatura. Esto significa un <strong>{ attendance.percentage }% 
          de asistencia justificada</strong> (considerando las inasistencias justificadas y las no justificadas)
          <sup><a id='text-attendance' href='#ref-1'>1</a></sup>.
        </p>
      </div>
    </>
  )
}

export default DeputyAttendance