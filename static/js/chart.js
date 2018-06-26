
function parseAttendance(att) {
    return [
        ['Asistencia', 'Valor'],
        ['Días asistidos', att['attended']],
        ['Días no asistidos sin justificar', att['unjustified']],
        ['Días no asistidos justificados', att['justified']]
    ];
}

function drawChart(title, array, id) {
    var data = google.visualization.arrayToDataTable(array);

    var options = {
        'title': title
    };

    var chart = new google.visualization.PieChart(document.getElementById(id));
    chart.draw(data, options);
}

attendance = parseAttendance(attendance);


google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(function () {
    drawChart('Asistencia', attendance, 'attendancechart');
});

