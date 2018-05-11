import urllib.request
from tqdm import tqdm
from bs4 import BeautifulSoup
import json
import os
import datetime

class Parser:
    def get_deputies(self):
        """
        Returns a list of lists containing information for every deputy, in the format:
        ['First Names', 'Surnames', 'Party','District', ['Attendance'], 'Birthday', 'Profession', ['Periods']]
        """
        deputies = self.__merge_depattinfo(self.__parse_personalinfo(), self.__parse_depattendance())
        for i in range(len(deputies)):
            deputy = dict()
            deputy["name"] = deputies[i][0]
            deputy["surname"] = deputies[i][1]
            deputy["party"] = deputies[i][2]
            deputy["district"] = deputies[i][3]
            deputy["attendance"] = deputies[i][4]
            deputy["photo"] = deputies[i][5]
            deputy["birthday"] = deputies[i][6]
            deputy["profession"] = deputies[i][7]
            deputy["periods"] = deputies[i][4]
            deputies[i] = deputy

        json_deputies = dict()
        json_deputies["deputies"] = deputies

        # Last modification date and time
        json_deputies["modified"] = str(datetime.datetime.now())

        # Current selected deputy's index (by default is the first one)
        json_deputies["current"] = dict(index=0, modified=str(datetime.datetime.now()))

        path = os.path.abspath('..') + '/static/json/deputies.json'

        with open(path, 'r') as infile:
            # Load file to check if exists a current deputy
            last_deputies = json.load(infile)
            if last_deputies["current"]:
                json_deputies["current"] = last_deputies["current"]
                infile.close()

        with open(path, 'w'):
            pass

        with open(path, 'w') as outfile:
            json.dump(json_deputies, outfile)
            outfile.close()

        return json_deputies

    def is_not_used(self):
        pass

    def __parse_personalinfo(self):
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

    def __parse_depattendance(self):
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
        for row in frows:
            formatted.append([])
            for td in row.findAll('td'):
                formatted[len(formatted)-1].append(td.getText().strip())
        formatted.pop(0)

        for i in tqdm(range(1, len(frows))):
            link = 'https://www.camara.cl' + frows[i].find('td').find('a')['href'][2:]
            profile = self.__parse_depprofile(link)
            for j in range(len(profile)):
                formatted[i-1].append(profile[j])

        return formatted

    def __merge_depattinfo(self, infolist, attlist):
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
                    attendance = []
                    for k in range(2, 5):
                        attendance.append(attlist[j][k])
                    infolist[i].append(attendance)

                    for k in range(5, len(attlist[j])):
                        infolist[i].append(attlist[j][k])

        return infolist

    def __parse_depprofile(self, link):
        self.is_not_used()
        quote_page = link
        page = urllib.request.urlopen(quote_page)

        soup = BeautifulSoup(page, 'html.parser')

        photo_link = 'https://www.camara.cl'
        photo_link += soup.findAll('div', attrs={'class': 'imgSet'})[1].find('img')['src']
        birthday = soup.find('div', attrs={'class': 'birthDate'}).find('p').getText().strip()
        profession = soup.find('div', attrs={'class': 'profession'}).find('p').getText().strip()
        periods = soup.findAll('div', attrs={'class': 'summary'})[1].findAll('li')
        for i in range(len(periods)):
            periods[i] = periods[i].getText().strip()

        profile = (photo_link, birthday, profession, periods)
        return profile

