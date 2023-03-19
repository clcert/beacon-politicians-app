from bs4 import BeautifulSoup
from datetime import datetime
import requests

from deputies.utils import get_current_legislature
from settings import (
    BASE_VOTINGS_LEGISLATURE_URL,
    BASE_VOTING_DETAIL_URL,
    BASE_BULLETIN_LAW_PROJECT_URL,
    VOTING_BLACKLIST,
)

def parse_deputy_votings(deputy_id, votes_limit=-1):
    """
    Method used to get vote information from all voting of the last legislature,
    :param deputy_id: Integer representing the deputy id.
    :return: Returns a list of dictionaries containing each one the name, description, date and the vote_option
        for a voting.
    """
    legislature_voting = get_legislature_votings()
    legislature_voting = sorted(legislature_voting, key=lambda k: k['date'], reverse=True)

    total_votes = len(legislature_voting)
    if votes_limit == -1:
        votes_limit = total_votes
    else:
        votes_limit = min(total_votes, votes_limit)

    ans = []
    
    for i in range(total_votes):
        if votes_limit == 0:
            break

        voting_id = legislature_voting[i]['voting_id']
        doc = parse_vote_info(voting_id)

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

        blacklist_matches = list(filter(
            lambda word: word in voting['name'].lower(), 
            VOTING_BLACKLIST
        ))

        if len(blacklist_matches) == 0:
            ans.append(voting)
            votes_limit -= 1

    return ans


def get_legislature_votings():
    """
    Obtains all voting from the latest legislature.
    :return: Returns a list of dictionary representing the information for every legislature, where each one
    has the voting_id, document, date and type of the voting.
    """
    legislature = get_current_legislature()

    start = legislature['start']
    start_year = int(start.year)

    url = BASE_VOTINGS_LEGISLATURE_URL + str(start_year)
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

    url = BASE_VOTINGS_LEGISLATURE_URL + str(end_year)
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
            voting_list.append(dict(voting_id=voting_id, description=description, date=date, type=type))

    return voting_list


def parse_vote_info(voting_id):
    """
    Method used to get document information, given a voting id.
    :param voting_id: Integer representing the voting id from the deputies chamber.
    :return: Returns a dictionary containing all the information for the voted document.
    """

    url = BASE_VOTING_DETAIL_URL + str(voting_id)
    response = requests.get(url)
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

        url = BASE_BULLETIN_LAW_PROJECT_URL + bulletin
        response = requests.get(url)
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
        if document['description'].startswith('OTROS-'):
            document['name'] = document['description'][6:]
        document['description'] = 'Otros'

    # name_length = len(document['name'])

    # if name_length > 200:
    #     document['name'] = document['name'][0:200] + "..."

    return document