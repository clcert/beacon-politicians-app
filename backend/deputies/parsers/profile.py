from bs4 import BeautifulSoup
from datetime import datetime
import requests

def parse_deputy_profile(html_url, xml_url):
    """
    Method used to scrap information from the profile of a deputy, given a deputy id.
    :param url: URL of the deputy's profile.
    :return: Returns basic information of the deputy.
    """
    response = requests.get(html_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    profile = {}

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

    raw_periods = general_section.findAll('div', attrs={'class': 'grid-2 aleft m-left14'})[-1].findAll('li')[1:]
    profile['periods'] = list(map(BeautifulSoup.getText, raw_periods))
    profile['lastperiod'] = profile['periods'][-1]

    response = requests.get(xml_url)
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

    return profile