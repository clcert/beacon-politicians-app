import urllib.request
from datetime import datetime
from bs4 import BeautifulSoup


class Parser:
    def __init__(self):
        self.profile_url = 'https://www.camara.cl/camara/diputado_detalle.aspx?prmID='
        self.services_url = 'http://opendata.camara.cl/camaradiputados/WServices/'
        self.deputies_url = 'https://www.camara.cl/camara/diputados_print.aspx'

    def get_deputy(self, deputy_index, votes=10):
        """
        Method used to get all information related to a deputy according to the given index.
        :param votes: Number of votes to be returned
        :param deputy_index: Index of the deputy. Belongs to the interval [0, count_deputies-1]
        :return: Returns a dictionary containing all deputy's information.
        """
        deputy_id = self.idfindex(deputy_index)
        profile = self.get_profile(deputy_id)
        profile['deputy_id'] =deputy_id
        profile['attendance'] = self.get_all_attendance(deputy_id)
        profile['voting'] = self.get_deputy_votes(deputy_id, votes)
        return profile

    def get_profile(self, deputy_id):
        """
        Method used to scrap information from the profile of a deputy, given a deputy id.
        :param deputy_id: Integer representing the deputy id.
        :return: Returns basic information of the deputy.
        """
        url = self.profile_url + str(deputy_id)
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')

        photo_link = 'https://www.camara.cl'
        photo_link += soup.findAll('div', attrs={'class': 'imgSet'})[1].find('img')['src']
        birthday = soup.find('div', attrs={'class': 'birthDate'}).find('p').getText().strip()
        profession = soup.find('div', attrs={'class': 'profession'}).find('p').getText().strip()
        if not profession:
            profession = 'Sin profesión'
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

        url = self.deputies_url
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')

        rows = soup.find('tbody').find_all('tr')
        for row in rows:
            name = row.find('td').get_text()
            if (profile['first_name'] in name) and (profile['first_surname'] in name):
                district = row.find_all('td')[2].get_text()
                district = int(district[2:len(district)])
                party = row.find_all('td')[3].get_text()
                profile['district'] = district
                profile['party'] = party
                break

        return profile

    def get_legislature(self):
        """
        Method used to get the information from the latest legislature.
        :return: Returns a dictionary containing the id of the latest legislature, and the date of end and start
                 as a datetime object.
        """
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
        """
        Method used to get a list containing the id for every session of the deputies chamber.
        :return: A list of integers, where each one represents the session id.
        """
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
        """
        Method used to get the total number of deputies on the current legislature.
        :return: Returns the total number of deputies as an integer.
        """
        url = self.services_url + 'WSDiputado.asmx/retornarDiputadosPeriodoActual'
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'lxml')

        deputies = soup.find_all('diputado')
        return len(deputies)

    def get_all_attendance(self, deputy_id):
        """
        Method used to get the attendance of a deputy for all the chamber sessions of the
        current legislature.
        :param deputy_id: Integer representing the deputy id.
        :return: Returns a dictionary containing the number of days attended, unattended justified or not, the total
        number of days and the official percentage of attended days.
        """
        justifications = self.get_justifications()

        sessions = self.get_sessions()
        url = self.services_url + 'WSSala.asmx/retornarSesionAsistencia?prmSesionId='

        deputy_attendance = dict(attended=0, justified=0, unjustified=0, total=0, percentage=100.0)
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
                        deputy_attendance['attended'] += 1

                    # If not, check the justification
                    else:
                        justification = attendance.find('justificacion')

                        if justification:
                            justification = justification['valor']
                            is_justified = not(justifications[int(justification)-1]['reductionattendance'])
                        else:
                            # Isn't justified if there isn't justification .
                            is_justified = 0

                        if is_justified:
                            deputy_attendance['justified'] += 1
                        else:
                            deputy_attendance['unjustified'] += 1
                    deputy_attendance['total'] += 1
                    break

        deputy_attendance['percentage'] *= (deputy_attendance['justified'] + deputy_attendance['attended'])
        deputy_attendance['percentage'] /= deputy_attendance['total']
        deputy_attendance['percentage'] = round(deputy_attendance['percentage'], 2)
        return deputy_attendance

    def get_justifications(self):
        """
        Method used to get the list of all possible justifications for non-attendance.
        :return: Returns a list containing dictionaries objects, where every dictionary contains the information for
                 a time of attendance value, as name, reduction of days and the value (the id according to the site).
        """
        url = self.services_url + 'WSComun.asmx/retornarTiposJustificacionesInasistencia'
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'lxml')

        justifications = soup.find_all('justificacioninasistencia')
        for i in range(len(justifications)):
            justification = dict()
            justification['name'] = justifications[i].find('nombre').get_text()
            justification['reductionattendance'] = 1 if justifications[i].find('rebajaasistencia').get_text() == 'true' else 0
            justification['value'] = justifications[i]['valor']
            justifications[i] = justification
        return justifications

    def idfindex(self, deputy_index):
        """
        Given a index between 0 and the total number of deputies, returns the id of a deputy, given a index.
        :param deputy_index: Index of the deputy, must be between 0 and the total number of deputies minus one.
        :return: Returns the id of the deputy, used in the deputies chamber.
        """
        url = self.services_url + 'WSDiputado.asmx/retornarDiputadosPeriodoActual'
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'lxml')

        deputies = soup.find_all('diputado')
        deputy = deputies[deputy_index]
        deputy_id = int(deputy.find('id').get_text())
        return deputy_id

    def get_legislature_voting(self, limit=-1):
        """
        Method used to get all voting from the latest legislature.
        :return: Returns a list of dictionary representing the information for every legislature, where each one
                 has the voting_id, document, date and type of the voting.
        """
        legislature = self.get_legislature()

        start = legislature['start']
        start_year = int(start.year)

        url = self.services_url + 'WSLegislativo.asmx/retornarVotacionesXAnno?prmAnno=' + str(start_year)
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'lxml')

        legislature_voting = list()

        all_voting = soup.find_all('votacion')
        if all_voting:
            for voting in all_voting:
                voting_date = voting.find('fecha').get_text()
                voting_date = datetime.strptime(voting_date, "%Y-%m-%dT%H:%M:%S")
                if voting_date < start:
                    continue
                else:
                    legislature_voting.append(voting)

        end = legislature['end']
        end_year = int(end.year)

        url = self.services_url + 'WSLegislativo.asmx/retornarVotacionesXAnno?prmAnno=' + str(end_year)
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'lxml')

        all_voting = soup.find_all('votacion')
        if all_voting:
            for voting in all_voting:
                voting_date = voting.find('fecha').get_text()
                voting_date = datetime.strptime(voting_date, "%Y-%m-%dT%H:%M:%S")
                if voting_date > end:
                    continue
                else:
                    legislature_voting.append(voting)

        voting_list = list()
        for voting in legislature_voting:
            voting_id = int(voting.find('id').get_text())
            description = voting.find('descripcion').get_text()
            date = datetime.strptime(voting.find('fecha').get_text(), "%Y-%m-%dT%H:%M:%S")
            type = int(voting.find('tipo')['valor'])

            # type = 1 -> 'Proyecto de Ley' (Boletines)
            # type = 2 -> 'Proyecto de Resolucion'
            # type = 3 -> 'Proyecto de acuerdo'
            # type = 4 -> 'Otros Documentos'

            if type != 1 and type != 4:
                continue
            else:
                voting_list.append(dict(voting_id=voting_id, description=description, date=date, type=type))
        if limit == -1:
            return voting_list
        else:
            voting_list = sorted(voting_list, key=lambda k: k['date'], reverse=True)
            return voting_list[0:min(limit, len(voting_list))]

    def get_document_info(self, voting_id):
        """
        Method used to get document information, given a voting id.
        :param voting_id: Integer representing the voting id from the deputies chamber.
        :return: Returns a dictionary containing all the information for the voted document.
        """

        url = self.services_url + 'WSLegislativo.asmx/retornarVotacionDetalle?prmVotacionId=' + str(voting_id)
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'lxml')

        document = dict(voting_id=voting_id)
        votes = soup.find_all('voto')
        for i in range(len(votes)):
            deputy_id = int(votes[i].find('id').get_text())
            vote_option = votes[i].find('opcionvoto').get_text()
            votes[i] = dict(deputy_id=deputy_id, vote_option=vote_option)
        document['votes'] = votes

        document['date'] = datetime.strptime(soup.find('fecha').get_text(), "%Y-%m-%dT%H:%M:%S")
        document['description'] = soup.find('descripcion').get_text()
        document['total_yes'] = int(soup.find('totalsi').get_text())
        document['total_no'] = int(soup.find('totalno').get_text())
        document['total_abstention'] = int(soup.find('totalabstencion').get_text())
        document['total_dispensed'] = int(soup.find('totaldispensado').get_text())
        document['quorum'] = soup.find('quorum').get_text()
        document['result'] = soup.find('resultado').get_text()
        document['type'] = int(soup.find('tipo')['valor'])

        if document['type'] == 1:    # Proyecto de Ley.
            # Get bulletin string.
            bulletin = document['description'][11:len(document['description'])]
            url = self.services_url + 'WSLegislativo.asmx/retornarProyectoLey?prmNumeroBoletin=' + bulletin
            page = urllib.request.urlopen(url)
            soup = BeautifulSoup(page, 'lxml')

            name = soup.find('nombre').get_text()
            document['name'] = name

        # elif document['type'] == 2: # Implement if necessary
        # elif document['type'] == 3: # Implement if necessary

        elif document['type'] == 4: # Otro documento
            document['name'] = document['description']
            document['description'] = 'Otros'

        if len(document['name']) > 150:
            i = 0
            while i < 150 or document['name'][i] != ' ':
                i += 1
            document['name'] = document['name'][0:i] + "..."

        return document

    def get_deputy_votes(self, deputy_id, limit=-1):
        """
        Method used to get vote information from all voting of the last legislature,
        :param deputy_id: Integer representing the deputy id.
        :return: Returns a list of dictionaries containing each one the name, description, date and the vote_option
                 for a voting.
        """
        legislature_voting = self.get_legislature_voting(limit)
        for i in range(len(legislature_voting)):
            voting_id = legislature_voting[i]['voting_id']
            doc = self.get_document_info(voting_id)

            voting = dict()

            votes = doc['votes']
            for vote in votes:
                if vote['deputy_id'] == deputy_id:
                    voting['vote_option'] = vote['vote_option']
                    break
            voting['date'] = doc['date'].strftime("%Y-%m-%d")
            voting['name'] = doc['name']
            voting['description'] = doc['description']
            voting['voting_id'] = doc['voting_id']
            legislature_voting[i] = voting
        return legislature_voting
