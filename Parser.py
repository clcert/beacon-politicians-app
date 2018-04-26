import urllib
from bs4 import BeautifulSoup

class Parser:
	def get_deputies(self):
		dep_list = self.parse_deplist()

		# Deputies list using format
		# ['First Names', 'Surnames', 'Birthdate', 'Party','Circunscription', 'Regions']
		deputies = [[dep_list[0][i], dep_list[1][i]] for i in range(len(dep_list[0]))]
		
		dep_info = dep_list[2]
		for i in range(len(deputies)):
			for j in range(len(dep_info[i])):
				deputies[i].append(dep_info[i][j])
		
		for i in range(len(deputies)):
			print(deputies[i])

	def parse_deplist(self):
		quote_page = 'https://www.camara.cl/camara/diputados_print.aspx'
		page = urllib.request.urlopen(quote_page)

		soup = BeautifulSoup(page, 'html.parser')

		deputies_table = soup.find('table', attrs={'class':'tabla'})

		rows = deputies_table.findAll('tr')
		full_names = []
		for row in rows:
			col = row.findAll('td')
			# If the row isn't empty, get deputy's name
			if len(col):
				name = col[0].getText()

				# Name without unecessary spaces or line breaks
				fixed_name = ""
				for i in range(len(name)):
					if name[i] > '!' or (name[i] == ' ' and name[i-1] != '\t'):
						fixed_name += name[i]
				fixed_name = fixed_name[1:len(fixed_name)]
				full_names.append(fixed_name)

		# Lists to separe first names from surnames
		surnames = []
		first_names = []
		for name in full_names:
			for i in range(len(name)):
				if name[i] == ',':
					surnames.append(name[0:i])
					first_names.append(name[(i+3):])
					break
		
		# Additional information ['Region', 'District', 'Party']
		additional_info = []
		for row in rows:
			col = row.findAll('td')

			if len(col):
				district = col[2].getText()
				party = col[3].getText()
				additional_info.append([district, party])

		return (first_names, surnames, additional_info)

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