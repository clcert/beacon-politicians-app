
function parseAttendance(att) {
    for (var i = 0; i < att[3].length; ++i) {
        if (att[3][i] === '%')
            att[3][i] = ' ';
    }
    att[3] = parseInt(att[3]);



    var justified = att[2] * (att[3]/100) - att[0];
    justified = parseInt(justified.toFixed());

    att[0] = ['Días asistidos', att[0]];
    att[1] = ['Días no asistidos sin justificar', Math.max(0, att[1] - justified)];
    att[2] = ['Días no asistidos justificados', justified];
    att = [['Descripción', 'Asistencia'], ...att];
    att.pop();

    return att;
}

function drawChart(title, array, id) {
    var data = google.visualization.arrayToDataTable(array);

    var options = {
        'title': title
    };

    console.log(array);
    var chart = new google.visualization.PieChart(document.getElementById(id));
    chart.draw(data, options);
}

attendance = parseAttendance(attendance);


google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(function () {
    drawChart('Asistencia', attendance, 'attendancechart');
});

