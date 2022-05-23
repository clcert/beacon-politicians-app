#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib.request
from datetime import datetime
from bs4 import BeautifulSoup


class Parser:
    def __init__(self):
        self.profile_url = 'https://www.camara.cl/diputados/detalle/biografia.aspx?prmId='
        self.services_url = 'http://opendata.camara.cl/camaradiputados/WServices/'
        # self.deputies_url = 'https://www.camara.cl/camara/diputados_print.aspx' 404

    def get_deputy(self, deputy_index, votes=10):
        """
        Method used to get all information related to a deputy according to the given index.
        :param votes: Number of votes to be returned
        :param deputy_index: Index of the deputy. Belongs to the interval [0, count_deputies-1]
        :return: Returns a dictionary containing all deputy's information.
        """
        deputy_id = self.idfindex(deputy_index)
        profile = self.get_profile(deputy_id)
        profile['deputy_id'] = deputy_id
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

        profile = {}

        profile['photo'] = 'https://www.camara.cl/img.aspx?prmID=GRCL' + str(deputy_id)

        general_section = soup.find('section', attrs={'id': 'info-ficha'})
        biography_section = soup.find('div', attrs={'class': 'biografia'})

        try:
            profession = biography_section.findAll('p')[2].getText().split('▪')[1].strip()
        except:
            profession = 'Sin Información'

        if len(profession) == 0:
            profession = 'Sin Información'
        profile['profession'] = profession.strip('.')

        main_info = general_section.find('div', attrs={'class': 'grid-3'}).getText().strip()
        main_info_list = list(map(str.strip, main_info.split('\r\n')))

        comunas = main_info_list[0].split(':')[1].strip()
        profile['district'] = main_info_list[1].split(':')[1].strip()
        profile['districtregion'] = main_info_list[2].split(':')[1].strip()
        profile['party'] = main_info_list[5].split(':')[1].strip()

        raw_periods = general_section.findAll('div', attrs={'class': 'grid-2 aleft m-left14'})[-1].findAll('li')[1:]
        profile['periods'] = list(map(BeautifulSoup.getText, raw_periods))
        profile['lastperiod'] = profile['periods'][-1]

        url = self.services_url + 'WSDiputado.asmx/retornarDiputado?prmDiputadoId=' + str(deputy_id)
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'xml')

        profile['first_name'] = soup.find('Nombre').get_text()
        profile['second_name'] = soup.find('Nombre2').get_text()

        profile['first_surname'] = soup.find('ApellidoPaterno').get_text()
        profile['second_surname'] = soup.find('ApellidoMaterno').get_text()

        profile['birthday'] = soup.find('FechaNacimiento').get_text()

        profile['sex'] = soup.find('Sexo')['Valor']
        profile['termination'] = 'o' if profile['sex'] == '1' else 'a'
        profile['treatment'] = 'Sr' if profile['sex'] == '1' else 'Sra'

        return profile

    def get_legislature(self):
        """
        Method used to get the information from the latest legislature.
        :return: Returns a dictionary containing the id of the latest legislature, and the date of end and start
                 as a datetime object.
        """
        url = self.services_url + 'WSLegislativo.asmx/retornarLegislaturaActual'
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'xml')

        id = int(soup.find('Id').get_text().strip())

        start = soup.find('FechaInicio').get_text()
        start = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")

        end = soup.find('FechaTermino').get_text()
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
        soup = BeautifulSoup(page, 'xml')

        sessions = soup.find_all('Sesion')

        # If a session hasn't been celebrated, pop it from the list.
        celebrated_sessions = list(filter(
            lambda session: session.find('Estado')['Valor'] == '1',
            sessions
        ))

        # Gets only session ids from the list.
        ids_cessions = list(map(
            lambda session: int(session.find('Id').get_text().strip()),
            celebrated_sessions
        ))

        return ids_cessions

    def count_deputies(self):
        """
        Method used to get the total number of deputies on the current legislature.
        :return: Returns the total number of deputies as an integer.
        """
        url = self.services_url + 'WSDiputado.asmx/retornarDiputadosPeriodoActual'
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'xml')

        deputies = soup.find_all('Diputado')
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
            session_url = url + str(session)
            page = urllib.request.urlopen(session_url)
            soup = BeautifulSoup(page, 'xml')

            # Only check attendance of the deputy we are looking for
            attendance = list(filter(
                lambda attendance: int(attendance.find('Id').get_text()) == deputy_id,
                soup.find_all('Asistencia')
            ))[0]
            
            attendance_type = attendance.find('TipoAsistencia')['Valor']

            # If deputy has gone to the session, we count it
            if attendance_type == '1':
                deputy_attendance['attended'] += 1

            # If not, check the justification
            else:
                justification = attendance.find('Justificacion')

                if justification:
                    is_justified = not(
                        justifications[int(justification['Valor'])-1]['ReductionAttendance']
                    )
                else:
                    # Isn't justified if there isn't justification .
                    is_justified = 0

                if is_justified:
                    deputy_attendance['justified'] += 1
                else:
                    deputy_attendance['unjustified'] += 1

        percentage = round(
            (deputy_attendance['justified'] + deputy_attendance['attended']) / len(sessions),
            2
        )    
        deputy_attendance['total'] = len(sessions)
        deputy_attendance['percentage'] *= percentage

        return deputy_attendance

    def get_justifications(self):
        """
        Method used to get the list of all possible justifications for non-attendance.
        :return: Returns a list containing dictionaries objects, where every dictionary contains the information for
                 a time of attendance value, as name, reduction of days and the value (the id according to the site).
        """
        url = self.services_url + 'WSComun.asmx/retornarTiposJustificacionesInasistencia'
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'xml')

        justifications = soup.find_all('JustificacionInasistencia')
        for i in range(len(justifications)):
            justification = dict()
            justification['name'] = justifications[i].find('Nombre').get_text()
            justification['reductionattendance'] = 1 if justifications[i].find('RebajaAsistencia').get_text() == 'true' else 0
            justification['value'] = justifications[i]['Valor']
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
        soup = BeautifulSoup(page, 'xml')

        deputies = soup.find_all('Diputado')
        deputy = deputies[deputy_index]
        deputy_id = int(deputy.find('Id').get_text())
        return deputy_id

    def get_legislature_voting(self):
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
        soup = BeautifulSoup(page, 'xml')

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

        return voting_list

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
        legislature_voting = self.get_legislature_voting()
        legislature_voting = sorted(legislature_voting, key=lambda k: k['date'], reverse=True)

        voting_limit = len(legislature_voting)
        if limit != -1:
            voting_limit = min(voting_limit, limit)

        ans = list()
        for i in range(len(legislature_voting)):
            if voting_limit == 0:
                break

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

            # Voting filter
            # Blacklist of keywords
            blacklist = list()
            blacklist.append([])
            blacklist[0].append('modifica')
            blacklist[0].append('ley')
            blacklist[0].append('n°')

            blacklist.append([])
            blacklist[1].append('solicita')
            blacklist[1].append('presidente')

            is_valid = True
            for i in range(len(blacklist)):
                cond = True
                for j in range(len(blacklist[i])):
                    cond = cond and (blacklist[i][j] in voting['name'].lower())
                if cond:
                    is_valid = False

            if is_valid:
                ans.append(voting)
                voting_limit -= 1

        return ans
