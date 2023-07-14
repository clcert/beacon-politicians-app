import React, { useEffect } from 'react';
import Chart from 'chart.js/auto';

const DeputyActivity = ({activity, gender, deputyId}) => {

  const depPronoun = gender === 'MALE' ? 'el diputado' : 'la diputada';
  const activityUrl = `https://www.camara.cl/diputados/detalle/mociones.aspx?prmId=${deputyId}`;
  
  useEffect(() => {
    var container = document.getElementById('activity-chart').getContext('2d');
    var activity_data = [
      activity.published, 
      activity.in_process, 
      activity.rejected,
      activity.unadmissible,
      activity.inconstitutional,
      activity.archived,
      activity.withdrawn,
    ];
    var activity_labels = [
      "Publicadas",
      "En trámite",
      "Rechazadas",
      "Inadmisibles",
      "Archivadas",
      "Retiradas",
      "Inconstitucionales",
    ];
    var activity_colors = [
      "#09F0B3",
      "#1898F2",
      "#F29018",
      "#FFE817",
      "#777777",
      "#BBBBBB",
      "#FF0000",
    ];
    var myChart = new Chart(container, {
      type: 'doughnut',
      data: {
        labels: activity_labels,
        datasets: [{
          label: "Mociones",
          borderRadius: 3,
          borderWidth: 2,
          backgroundColor: activity_colors,
          data: activity_data,
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
            text: 'Mociones Parlamentarias',
            font: {
              size: 20,
            }
          }
        }
      }
    });

    return () => myChart.destroy();
  
  }, [activity])

  return (
    <>
      <div className='image chart-container-1'>
        <canvas id='activity-chart' height='100%'></canvas>
      </div>
      <div className="content">
        <p>
          A lo largo de su período parlamentario, { depPronoun } ha presentado <strong>{ activity.all } proyectos de ley</strong>,
          de las cuales <strong>{ activity.published } han sido publicadas</strong> y <strong>{ activity.in_process } se encuentran en trámite</strong>
          <sup><a id='text-attendance' href='#ref-1'>2</a></sup>.
        </p>
        <p>
          Puedes revisar el detalle de los proyectos de ley presentados por { depPronoun } en el siguiente <a href={activityUrl} target='_blank'>enlace</a>.
        </p>
      </div>
    </>
  )
}

export default DeputyActivity