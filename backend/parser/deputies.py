#!/usr/bin/env python
import requests as req
from datetime import datetime
from bs4 import BeautifulSoup
from .expenses import OfficesExpensesParser, OperationalExpensesParser, StaffExpensesParser
from time import perf_counter


class Parser:
    def __init__(self):
        self.profile_url = 'https://www.camara.cl/diputados/detalle/biografia.aspx?prmId='
        self.services_url = 'http://opendata.camara.cl/camaradiputados/WServices/'

    def get_deputy(self, deputy_index, votes=10):
        """
        Method used to get all information related to a deputy according to the given index.
        :param votes: Number of votes to be returned
        :param deputy_index: Index of the deputy. Belongs to the interval [0, count_deputies-1]
        :return: Returns a dictionary containing all deputy's information.
        """
        print(f'{datetime.today()}\nLoading new deputy...\n')
        t_0 = perf_counter()

        deputy_id = self.idfindex(deputy_index)
        profile = self.get_profile(deputy_id)
        print(f'Obtaining Information for: {profile["first_name"]} {profile["first_surname"]}')
        profile['deputy_id'] = deputy_id
        print(f'Main profile obtained\n-- Elapsed time: {round(perf_counter() - t_0, 3)}s')

        profile['attendance'] = self.get_all_attendance(deputy_id)
        print(f'Deputy attendance obtained\n-- Elapsed time: {round(perf_counter() - t_0, 3) }s')

        profile['voting'] = self.get_deputy_votes(deputy_id, votes)
        print(f'Deputy voting obtained\n-- Elapsed time: {round(perf_counter() - t_0, 3)}s')

        profile['expenses'] = self.get_deputy_expenses(profile)
        print(f'Deputy expenses obtained\n-- Elapsed time: {round(perf_counter() - t_0, 3)}s')

        return profile

    def get_profile(self, deputy_id):
        """
        Method used to scrap information from the profile of a deputy, given a deputy id.
        :param deputy_id: Integer representing the deputy id.
        :return: Returns basic information of the deputy.
        """
        url = self.profile_url + str(deputy_id)
        response = req.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        profile = {}

        profile['photo'] = 'https://www.camara.cl/img.aspx?prmID=GRCL' + str(deputy_id)

        general_section = soup.find('section', attrs={'id': 'info-ficha'})
        biography_section = soup.find('div', attrs={'class': 'biografia'})

        try:
            profession = biography_section.findAll('p')[2].getText().split('▪')[1].strip()
        except:
            profession = 'Sin Información'

        if len(profession) == 0 or len(profession) > 50:
            profession = 'Sin Información'

        profile['profession'] = profession.strip('.')

        main_info = general_section.find('div', attrs={'class': 'grid-3'}).getText().strip()
        main_info_list = list(map(str.strip, main_info.split('\r\n')))

        comunas = main_info_list[0].split(':')[1].strip()
        profile['district'] = main_info_list[1].split(':')[1].strip()
        profile['districtregion'] = main_info_list[2].split(':')[1].strip()
        #profile['party'] = main_info_list[5].split(':')[1].strip()

        raw_periods = general_section.findAll('div', attrs={'class': 'grid-2 aleft m-left14'})[-1].findAll('li')[1:]
        profile['periods'] = list(map(BeautifulSoup.getText, raw_periods))
        profile['lastperiod'] = profile['periods'][-1]

        url = self.services_url + 'WSDiputado.asmx/retornarDiputado?prmDiputadoId=' + str(deputy_id)
        response = req.get(url)
        soup = BeautifulSoup(response.content, 'xml')

        profile['first_name'] = soup.find('Nombre').get_text()
        profile['second_name'] = soup.find('Nombre2').get_text()

        profile['first_surname'] = soup.find('ApellidoPaterno').get_text()
        profile['second_surname'] = soup.find('ApellidoMaterno').get_text()
        current_party = soup.find_all('Militancia')[0]
        profile['party'] = current_party.find('Nombre').get_text()
        profile['party_alias'] = current_party.find('Alias').get_text()


        raw_birthday = datetime.strptime(
            soup.find('FechaNacimiento').get_text(),
            '%Y-%m-%dT%H:%M:%S'
        )
        profile['birthday'] = datetime.strftime(raw_birthday, '%d/%m/%Y')

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
        response = req.get(url)
        soup = BeautifulSoup(response.content, 'xml')

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
        response = req.get(url)
        soup = BeautifulSoup(response.content, 'xml')

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
        response = req.get(url)
        soup = BeautifulSoup(response.content, 'xml')

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
            response = req.get(session_url)
            soup = BeautifulSoup(response.content, 'xml')

            # If there is no register of attendance we skip this session
            if not soup.find('Asistencia'):
                continue

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
                        justifications[int(justification['Valor'])-1]['reductionattendance']
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
        response = req.get(url)
        soup = BeautifulSoup(response.content, 'xml')

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
        response = req.get(url)
        soup = BeautifulSoup(response.content, 'xml')

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
        response = req.get(url)
        soup = BeautifulSoup(response.content, 'xml')

        legislature_voting_start = list(filter(
            lambda v: datetime.strptime(
                v.find('Fecha').get_text(),
                "%Y-%m-%dT%H:%M:%S"
            ) >= start,
            soup.find_all('Votacion')
        ))

        end = legislature['end']
        end_year = int(end.year)

        url = self.services_url + 'WSLegislativo.asmx/retornarVotacionesXAnno?prmAnno=' + str(end_year)
        response = req.get(url)
        soup = BeautifulSoup(response.content, 'xml')

        legislature_voting_end = list(filter(
            lambda v: datetime.strptime(
                v.find('Fecha').get_text(),
                "%Y-%m-%dT%H:%M:%S"
            ) <= end,
            soup.find_all('Votacion')
        ))

        legislature_voting = legislature_voting_start + legislature_voting_end
        
        voting_list = list()
        for voting in legislature_voting:
            voting_id = int(voting.find('Id').get_text())
            description = voting.find('Descripcion').get_text()
            date = datetime.strptime(voting.find('Fecha').get_text(), "%Y-%m-%dT%H:%M:%S")
            type = int(voting.find('Tipo')['Valor'])

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
        response = req.get(url)
        soup = BeautifulSoup(response.content, 'xml')

        document = dict(voting_id=voting_id)

        votes = list(map(
            lambda vote: dict(
                deputy_id = int(vote.find('Id').get_text()),
                vote_option = vote.find('OpcionVoto').get_text()
            ),
            soup.find_all('Voto')
        ))
        
        document['votes'] = votes
        document['date'] = datetime.strptime(soup.find('Fecha').get_text(), "%Y-%m-%dT%H:%M:%S")
        document['description'] = soup.find('Descripcion').get_text()
        document['total_yes'] = int(soup.find('TotalSi').get_text())
        document['total_no'] = int(soup.find('TotalNo').get_text())
        document['total_abstention'] = int(soup.find('TotalAbstencion').get_text())
        document['total_dispensed'] = int(soup.find('TotalDispensado').get_text())
        document['quorum'] = soup.find('Quorum').get_text()
        document['result'] = soup.find('Resultado').get_text() if soup.find('Resultado') != None else 'Desconocido'
        document['type'] = int(soup.find('Tipo')['Valor'])

        if document['type'] == 1:    # Proyecto de Ley.
            # Get bulletin string.
            bulletin = document['description'][11:]

            url = self.services_url + 'WSLegislativo.asmx/retornarProyectoLey?prmNumeroBoletin=' + bulletin
            response = req.get(url)
            soup = BeautifulSoup(response.content, 'xml')

            document['name'] = soup.find('Nombre').get_text()
            voting_instance = list(filter(
                lambda voting: voting.find('Id').get_text() == str(voting_id), 
                soup.findAll('VotacionProyectoLey')
            ))
            if len(voting_instance) > 0:
                document['article'] = voting_instance[0].find('Articulo').get_text().replace('\n', '')

        # elif document['type'] == 2: # Implement if necessary
        # elif document['type'] == 3: # Implement if necessary

        elif document['type'] == 4: # Otro documento
            document['name'] = document['description']
            document['description'] = 'Otros'

        name_length = len(document['name'])
        # if name_length > 200:
        #     document['name'] = document['name'][0:200] + "..."

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

            try:
                deputy_vote = list(filter(
                    lambda vote: vote['deputy_id'] == deputy_id,
                    doc['votes']
                ))[0]
            except:
                # No votó
                continue

            voting['vote_option'] = deputy_vote['vote_option']
            voting['date'] = doc['date'].strftime("%Y-%m-%d")
            voting['name'] = doc['name']
            voting['description'] = doc['description']
            voting['article'] = doc['article'] if 'article' in doc else 'No se encontró el artículo'
            voting['voting_id'] = doc['voting_id']
            voting['result'] = doc['result']
            voting['total_yes'] = doc['total_yes']
            voting['total_no'] = doc['total_no']
            voting['total_abstention'] = doc['total_abstention']
        

            # Voting filter
            # Blacklist of keywords
            blacklist = [
                'modifica',
                'ley',
                'n°',
                'solicita',
                'presidente'
            ]

            blacklist_matches = list(filter(
                lambda word: word in voting['name'].lower(), 
                blacklist
            ))

            if len(blacklist_matches) == 0:
                ans.append(voting)
                voting_limit -= 1

        return ans

    def get_deputy_expenses(self, profile):
        print('Getting expenses for deputy: ' + profile['first_name'])

        operational_parser = OperationalExpensesParser(profile)
        operational_expenses = operational_parser.get_deputy_expenses()
        if operational_expenses == []:
            print('(1/3) !! No operational expenses where found.')
        else:
            print('(1/3) Operational expenses obtained.')

        offices_parser = OfficesExpensesParser(profile)
        offices_expenses = offices_parser.get_deputy_expenses()
        if offices_expenses == []:
            print('(2/3) !! No offices expenses where found.')
        else:
            print('(2/3) Offices expenses obtained.')

        staff_parser = StaffExpensesParser(profile)
        staff_expenses = staff_parser.get_deputy_expenses()
        if staff_expenses == []:
            print('(3/3) !! No staff expenses where found.')
        else:
            print('(3/3) Staff expenses obtained.')

        return {
            'operational': operational_expenses,
            'offices': offices_expenses,
            'staff': staff_expenses,
        }
