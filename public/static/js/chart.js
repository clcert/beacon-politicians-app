var ctx = document.getElementById("myChart").getContext('2d');
var att = [attendance['attended'], attendance['justified'], attendance['unjustified']];
var myChart = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: ["Días Asistidos", "Días no asistidos justificados", "Días no asistidos no justificados"],
      datasets: [{
        label: "Population (millions)",
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