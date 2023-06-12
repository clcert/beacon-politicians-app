import React, { useEffect } from 'react';
import Chart from 'chart.js/auto';

const DeputyAttendance = ({data}) => {

  const depPronoun = data.termination === 'o' ? 'el diputado' : 'la diputada';

  useEffect(() => {
    var container = document.getElementById('attendances-chart').getContext('2d');
    var attendances_data = [
      data.attendance.attended, 
      data.attendance.justified, 
      data.attendance.unjustified
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
  
  }, [data])

  return (
    <>
      <div className='image chart-container-1'>
        <canvas id='attendances-chart' height='100%'></canvas>
      </div>
      <div className="content">
        <p>
          A la fecha, { depPronoun } ha asistido a <strong>{ data.attendance.attended } sesiones de cámara</strong>, 
          de un total de { data.attendance.total } sesiones dentro de la legislatura. Esto significa un <strong>{ data.attendance.percentage }% 
          de asistencia justificada</strong> (considerando las inasistencias justificadas y las no justificadas)
          <sup><a id='text-attendance' href='#ref-1'>1</a></sup>.
        </p>
      </div>
    </>
  )
}

export default DeputyAttendance