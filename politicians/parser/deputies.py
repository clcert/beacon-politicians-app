import urllib.request
from datetime import datetime
from bs4 import BeautifulSoup


class Parser:
    def __init__(self):
        self.profile_url = 'https://www.camara.cl/camara/diputado_detalle.aspx?prmID='
        self.services_url = 'http://opendata.camara.cl/camaradiputados/WServices/'

    def get_deputy(self, deputy_index):
        deputy_id = self.idfindex(deputy_index)
        profile = self.get_profile(deputy_id)
        attendance = self.get_all_attendance(deputy_id)
        profile['attendance'] = attendance
        return profile

    def get_profile(self, deputy_id):
        url = self.profile_url + str(deputy_id)
        page = urllib.request.urlopen(url)
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

        url = self.services_url + 'WSDiputado.asmx/retornarDiputado?prmDiputadoId=' + str(deputy_id)
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'lxml')

        profile['first_name'] = soup.find('nombre').get_text()
        profile['second_name'] = soup.find('nombre2').get_text()
        profile['first_surname'] = soup.find('apellidopaterno').get_text()
        profile['second_surname'] = soup.find('apellidomaterno').get_text()
        profile['sex'] = soup.find('sexo')['valor']
        profile['termination'] = 'o' if profile['sex'] == '1' else 'a'
        profile['treatment'] = 'Sr' if profile['sex'] == '1' else 'Sra'
        return profile

    def get_legislature(self):
        url = self.services_url + 'WSLegislativo.asmx/retornarLegislaturaActual'
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'lxml')

        id = int(soup.find('id').get_text().strip())

        start = soup.find('fechainicio').get_text()
        start = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")

        end = soup.find('fechatermino').get_text()
        end = datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")
        return dict(id=id, start=start, end=end)

    def get_sessions(self):
        url = self.services_url + 'WSSala.asmx/retornarSesionesXLegislatura?prmLegislaturaId=' + \
              str(self.get_legislature()['id'])
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'lxml')

        sessions = soup.find_all('sesion')

        # If a session hasn't been celebrated, pop it from the list.
        for session in sessions:
            if int(session.find('estado')['valor']) != 1:
                sessions.pop()

        # Gets only session ids from the list.
        for i in range(len(sessions)):
            sessions[i] = int(sessions[i].find('id').get_text().strip())
        return sessions

    def count_deputies(self):
        url = self.services_url + 'WSDiputado.asmx/retornarDiputadosPeriodoActual'
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'lxml')

        deputies = soup.find_all('diputado')
        return len(deputies)

    def get_all_attendance(self, deputy_id):
        justifications = self.get_justifications()

        sessions = self.get_sessions()
        url = self.services_url + 'WSSala.asmx/retornarSesionAsistencia?prmSesionId='

        deputy_attendance = dict(presence=0, justified=0, unjustified=0, total=0)
        for session in sessions:
            page = urllib.request.urlopen(url + str(session))
            soup = BeautifulSoup(page, 'lxml')

            attendances = soup.find_all('asistencia')
            for attendance in attendances:
                # Get the id of the attendance from the current deputy
                curr_id = int(attendance.find('id').get_text())

                # If current deputy is the deputy we're looking for, check attendance
                if curr_id == deputy_id:
                    attendance_type = attendance.find('tipoasistencia')['valor']

                    # If he has gone to the session, we count it
                    if attendance_type == '1':
                        deputy_attendance['presence'] += 1

                    # If not, check the justification
                    else:
                        justification = attendance.find('justificacion')

                        if justification:
                            justification = justification['valor']
                            is_justified = not(justifications[int(justification)-1]['rebajaasistencia'])
                        else:
                            # Isn't justified if there isn't justification .
                            is_justified = 0

                        if is_justified:
                            deputy_attendance['justified'] += 1
                        else:
                            deputy_attendance['unjustified'] += 1
                    deputy_attendance['total'] += 1
                    break

        deputy_attendance['percentage'] = 100.0 * (deputy_attendance['justified'] + deputy_attendance['presence'])
        deputy_attendance['percentage'] /= deputy_attendance['total']
        deputy_attendance['percentage'] = round(deputy_attendance['percentage'], 2)
        return deputy_attendance

    def get_justifications(self):
        url = self.services_url + 'WSComun.asmx/retornarTiposJustificacionesInasistencia'
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'lxml')

        justifications = soup.find_all('justificacioninasistencia')
        for i in range(len(justifications)):
            justification = dict()
            justification['nombre'] = justifications[i].find('nombre').get_text()
            justification['rebajaasistencia'] = 1 if justifications[i].find('rebajaasistencia').get_text() == 'true' else 0
            justification['valor'] = justifications[i]['valor']
            justifications[i] = justification
        return justifications

    def idfindex(self, deputy_index):
        url = self.services_url + 'WSDiputado.asmx/retornarDiputadosPeriodoActual'
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'lxml')

        deputies = soup.find_all('diputado')
        deputy = deputies[deputy_index]
        deputy_id = int(deputy.find('id').get_text())
        return deputy_id

    def get_all_voting(self, year):
        url = self.services_url + 'WSLegislativo.asmx/retornarVotacionesXAnno?prmAnno=' + str(year)
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'lxml')

        


if __name__ == '__main__':
    p = Parser()
    print(p.get_all_voting(2018))