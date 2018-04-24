import urllib
from bs4 import BeautifulSoup

class Parser:
	def get_deputies(self):
		full_names = self.parse_depnames()

		# Deputies list using format
		# ['First Names', 'Surnames', 'Birthdate', 'Party','Circunscription', 'Regions']
		deputies = [[full_names[0][i], full_names[1][i]] for i in range(len(full_names[0]))]

		for deputie in deputies:
			print(deputie)


	def parse_depnames(self):
		quote_page = 'https://www.camara.cl/camara/diputados_print.aspx'
		page = urllib.request.urlopen(quote_page)

		soup = BeautifulSoup(page, 'html.parser')

		deputies_table = soup.find('table', attrs={'class':'tabla'})

		rows = deputies_table.findAll('tr')
		full_names = []
		for row in rows:
			col = row.findAll('td')

			if len(col):
				name = col[0].getText()
				fixed_name = ""
				for i in range(len(name)):
					if name[i] > '!' or (name[i] == ' ' and name[i-1] != '\t'):
						fixed_name += name[i]
				fixed_name = fixed_name[1:len(fixed_name)]
				full_names.append(fixed_name)

		surnames = []
		first_names = []
		for name in full_names:
			for i in range(len(name)):
				if name[i] == ',':
					surnames.append(name[0:i])
					first_names.append(name[(i+3):])
					break
		
		return (first_names, surnames)

	def parse_depattendance():
		quote_page = 'https://www.camara.cl/trabajamos/sala_asistencia.aspx'
		page = urllib.request.urlopen(quote_page)

		soup = BeautifulSoup(page, 'html.parser')


		# Table containing Deputies Attendance Percentage
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
		return formatted


			
p = Parser()
p.get_deputies()