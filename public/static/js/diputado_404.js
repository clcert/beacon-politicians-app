var date = window.location.pathname.split('/').pop().split('.')[0];
var year = date.substring(0,4);
var month = date.substring(4,6);
var day = date.substring(6);
var curr_date = new Date(year, month, day);
var yesterday = new Date(new Date().setDate(curr_date.getDate() - 1));
var yesterday_year = '' + yesterday.getFullYear();
var yesterday_month = '' + (yesterday.getMonth() + 1);
if (yesterday_month.length < 2) {
	yesterday_month = '0' + yesterday_month;
}
var yesterday_day = '' + yesterday.getDate();
if (yesterday_day.length < 2) {
	yesterday_day = '0' + yesterday_day;
}
var full_yesterday_date = yesterday_year + yesterday_month + yesterday_day;

var div = document.getElementById('hola');
var new_url = document.createElement('a');
new_url.setAttribute('href', '/diputadodeldia/' + full_yesterday_date + '.html');
new_url.text = '#DiputadoDelDia anterior';
div.appendChild(new_url);

console.log(full_yesterday_date);
