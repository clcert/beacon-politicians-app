import urllib
from bs4 import BeautifulSoup

quote_page = 'https://www.camara.cl/trabajamos/sala_asistencia.aspx'
page = urllib.request.urlopen(quote_page)

soup = BeautifulSoup(page, 'html.parser')

my_table = soup.find('table', attrs={'class':'tabla'})
rows = my_table.findAll('tr')



for row in rows:
	if row.table:
		row.table.decompose()
	if row.div:
			row.div.decompose()	

frows = []
for row in rows:
	if len(row) != 0:
		frows.append(row)

formatted = []
for row in frows:
	formatted.append([])
	for td in row.findAll('td'):
		formatted[len(formatted)-1].append(td.getText().strip())
		
formatted[0] = ['Diputado', 'Partido', 'Asistencias', 'Inasistenicas', 'Porcentaje asistencia']
for form in formatted:
	print(form)