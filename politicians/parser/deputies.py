import urllib.request
from bs4 import BeautifulSoup


class Parser:
    def get_deputy(self, index):
        deputies = self.get_deputies()
        index = index % len(deputies)

        deputy = deputies[index]
        profile = self.parse_depprofile(deputy['link'])
        for key in profile:
            deputy[key] = profile[key]
        return deputy

    def get_deputies(self):
        """
        Returns a list of lists containing information for every deputy, in the format:
        ['First Names', 'Surnames', 'Party','District', ['Attendance'], 'Birthday', 'Profession', ['Periods']]
        """
        deputies = self.merge_depattinfo(self.parse_personalinfo(), self.parse_depattendance())
        for i in range(len(deputies)):
            deputy = dict()
            deputy['name'] = deputies[i][0]
            deputy['surname'] = deputies[i][1]
            deputy['party'] = deputies[i][2]
            deputy['district'] = deputies[i][3]

            deputy['treatment'] = deputies[i][4]
            deputy['gender'] = 'a' if len(deputies[i][4]) > 2 else 'o'

            deputy['attendance'] = deputies[i][5]
            total_sesions = int(deputy['attendance'][0]) + int(deputy['attendance'][1])
            deputy['attendance'] = [int(deputy['attendance'][0]), int(deputy['attendance'][1]), total_sesions,
                                    deputy['attendance'][2]]

            deputy['link'] = deputies[i][6]
            deputies[i] = deputy
        return deputies

    def is_not_used(self):
        pass

    def parse_personalinfo(self):
        self.is_not_used()
        quote_page = 'https://www.camara.cl/camara/diputados_print.aspx'
        page = urllib.request.urlopen(quote_page)

        soup = BeautifulSoup(page, 'html.parser')

        deputies_table = soup.find('table', attrs={'class': 'tabla'})

        rows = deputies_table.findAll('tr')
        full_names = []
        for row in rows:
            col = row.findAll('td')
            # If the row isn't empty, get deputy's name
            if len(col):
                name = col[0].getText()

                # Name without unnecessary spaces or line breaks
                fixed_name = ""
                for i in range(len(name)):
                    if name[i] > '!' or (name[i] == ' ' and name[i-1] != '\t'):
                        fixed_name += name[i]
                fixed_name = fixed_name[1:len(fixed_name)]
                full_names.append(fixed_name)

        # Lists to separate first names from surnames
        surnames = []
        first_names = []
        for name in full_names:
            for i in range(len(name)):
                if name[i] == ',':
                    surnames.append(name[0:i])
                    first_names.append(name[(i+3):])
                    break

        # District and party for every deputy
        district = []
        party = []
        for row in rows:
            col = row.findAll('td')

            if len(col):
                district.append(col[2].getText()[2:])
                party.append(col[3].getText())

        dep_list = (first_names, surnames, party, district)
        deputies = [[] for i in range(len(dep_list[0]))]

        for i in range(len(deputies)):
            for j in range(len(dep_list)):
                deputies[i].append(dep_list[j][i])
        return deputies

    def parse_depattendance(self):
        quote_page = 'https://www.camara.cl/trabajamos/sala_asistencia.aspx'
        page = urllib.request.urlopen(quote_page)

        soup = BeautifulSoup(page, 'html.parser')

        # Table containing Deputies Attendance Percentage
        my_table = soup.find('table', attrs={'class': 'tabla'})
        rows = my_table.findAll('tr')

        # Get rows without unnecessary info
        for row in rows:
            if row.table:
                row.table.decompose()
            if row.div:
                row.div.decompose()

        # Filter non empty rows
        frows = []
        for row in rows:
            if len(row):
                frows.append(row)

        formatted = []
        for i in range(1, len(frows)):
            formatted.append([])
            for td in frows[i].findAll('td'):
                formatted[len(formatted)-1].append(td.getText().strip())
            link = 'https://www.camara.cl' + frows[i].find('td').find('a')['href'][2:]
            formatted[len(formatted)-1].append(link)
    
        return formatted

    def merge_depattinfo(self, infolist, attlist):
        self.is_not_used()
        # For every element in infolist and attlist, we search for
        # a match between the first name in infolist and attlist and
        # the first surname for both.
        for i in range(len(infolist)):

            # Filter only the first surname
            first_surname = ""
            for c in infolist[i][1]:
                if c == " ":
                    break
                first_surname += c

            for j in range(len(attlist)):

                # If the first name and first surname is in the string, do something.
                if (infolist[i][0] in attlist[j][0]) and (first_surname in attlist[j][0]):
                    treatment = ""
                    for c in attlist[j][0]:
                        if c == '.':
                            break
                        treatment += c
                    infolist[i].append(treatment)

                    attendance = []
                    for k in range(2, 5):
                        attendance.append(attlist[j][k])
                    infolist[i].append(attendance)

                    for k in range(5, len(attlist[j])):
                        infolist[i].append(attlist[j][k])

        return infolist

    def parse_depprofile(self, link):
        self.is_not_used()
        quote_page = link
        page = urllib.request.urlopen(quote_page)

        soup = BeautifulSoup(page, 'html.parser')

        photo_link = 'https://www.camara.cl'
        photo_link += soup.findAll('div', attrs={'class': 'imgSet'})[1].find('img')['src']
        birthday = soup.find('div', attrs={'class': 'birthDate'}).find('p').getText().strip()
        profession = soup.find('div', attrs={'class': 'profession'}).find('p').getText().strip()
        if len(profession) > 0 and profession[len(profession)-1] == '.':
            profession = profession[0:len(profession)-1]

        dregion = soup.findAll('div', attrs={'class': 'summary'})[0].findAll('p')[2].getText().strip()
        districtregion = ""
        for i in range(len(dregion)):
            if dregion[i] > '!':
                districtregion += dregion[i]
            elif i > 0 and dregion[i] < '!' < dregion[i-1]:
                districtregion += ' '

        periods = soup.findAll('div', attrs={'class': 'summary'})[1].findAll('li')
        for i in range(len(periods)):
            periods[i] = periods[i].getText().strip()

        profile = dict(photo=photo_link, birthday=birthday, profession=profession, periods=periods,
                       districtregion=districtregion, lastperiod=periods[len(periods)-1])
        return profile
