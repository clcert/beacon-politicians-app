from utils.utils import get_current_legislature
from collectors.access_points import OpenDataAPI
from models.models import Bulletin, DeputyVoting
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

VOTINGS_TIMEOUT = 3

class VotingCollector:
    def __init__(self, deputy_id):
        self.deputy_id = deputy_id
    
    def get_legislature_votings(self):
        """
        Obtains all voting from the latest legislature.
        :return: Returns a list of dictionary representing the information for every legislature, where each one
        has the voting_id, document, date and type of the voting.
        """
        legislature = get_current_legislature()

        start = legislature['start']
        start_year = int(start.year)

        url = f"{OpenDataAPI.votings_legislature}?prmAnno={start_year}"
        response = requests.get(url)

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

        url = f"{OpenDataAPI.votings_legislature}?prmAnno={end_year}"
        response = requests.get(url)
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
                voting_list.append(
                    dict(
                        voting_id=voting_id,
                        description=description,
                        date=date,
                        type=type
                    )
                )

        return voting_list

    def parse_vote_info(self, voting_id):
        """
        Method used to get document information, given a voting id.
        :param voting_id: Integer representing the voting id from the deputies chamber.
        :return: Returns a dictionary containing all the information for the voted document.
        """

        url = f"{OpenDataAPI.voting_detail}?prmVotacionId={voting_id}"
        try:
            response = requests.get(url, timeout=VOTINGS_TIMEOUT)
            soup = BeautifulSoup(response.content, 'xml')
        except:
            raise Exception('Error al obtener la votación')

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

            url = f"{OpenDataAPI.bulletin_law_project}?prmNumeroBoletin={bulletin}"
            try:
                response = requests.get(url, timeout=VOTINGS_TIMEOUT)
                soup = BeautifulSoup(response.content, 'xml')
            except:
                raise Exception('Error al obtener el boletín del proyecto de ley')

            document['name'] = soup.find('Nombre').get_text()
            document['bulletin_id'] = int(soup.find('Id').get_text())
            blacklist_matches = list(filter(
                lambda word: word in document['name'].lower(), 
                VOTING_BLACKLIST
            ))

            if len(blacklist_matches) != 0:
                raise Exception('Voting name contains blacklisted words')

            voting_instance = list(filter(
                lambda voting: voting.find('Id').get_text() == str(voting_id), 
                soup.findAll('VotacionProyectoLey')
            ))
            
            if len(voting_instance) > 0:
                document['article'] = voting_instance[0].find('Articulo').get_text().replace('\n', '')

        elif document['type'] == 4: # Otro documento
            document['name'] = document['description']
            if document['description'].startswith('OTROS-'):
                document['name'] = document['description'][6:]
            document['description'] = 'Otros'

        return document

    
    def get_votings(self, votes_limit=-1):
        """
        Method used to get vote information from all voting of the last legislature,
        where the deputy voted.
        :param votes_limit: Integer representing the maximum number of votes to get.
        """
        legislature_voting = self.get_legislature_votings()
        legislature_voting = sorted(legislature_voting, key=lambda k: k['date'], reverse=True)

        total_votes = len(legislature_voting)
        if votes_limit == -1:
            votes_limit = total_votes
        else:
            votes_limit = min(total_votes, votes_limit)

        votings = []
        
        for i in range(total_votes):
            if votes_limit == 0:
                break

            voting_id = legislature_voting[i]['voting_id']
            try:
                doc = self.parse_vote_info(voting_id)
            except:
                # Error al obtener la votación o el documento no es un proyecto de ley
                continue

            voting = dict()

            try:
                deputy_vote = list(filter(
                    lambda vote: vote['deputy_id'] == self.deputy_id,
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
            voting['voting_id'] = int(voting_id)
            voting['result'] = doc['result']
            voting['total_yes'] = doc['total_yes']
            voting['total_no'] = doc['total_no']
            voting['total_abstention'] = doc['total_abstention']

            votes_limit -= 1
            votings.append(voting)

        self.votings = votings


    def save_votings(self):
        """
        Method used to save the votings of the deputy in the database.
        """
        for voting in self.votings:
            # TODO: there is a problem if no bulletin is found
            bulletin = Bulletin(
                id=bulletin_id,
                date=voting['date'],
                bulletin_title=voting['name'],
                bulletin_description=voting['description'],
                bulletin_status=voting['result'],
                approval_votes=voting['total_yes'],
                rejection_votes=voting['total_no'],
                abstention_votes=voting['total_abstention']
            )
            Bulletin.save_or_update(bulletin)

            deputy_voting = DeputyVoting(
                id=voting['voting_id'],
                deputy_id=self.deputy_id,
                bulletin_id=bulletin_id,
                vote=voting['vote_option']
            )
            DeputyVoting.save_or_update(deputy_voting)