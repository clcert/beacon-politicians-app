from collectors.access_points import OpenDataAPI, CamaraCL
from models.models import Deputy, DeputyPeriod
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class ProfileCollector:
    def __init__(self, local_id):
        self.local_id = local_id
        self.id = self.get_real_id(local_id)
        self.profile_url = f'{CamaraCL.biography}?prmId={self.id}'
        self.profile = {
            'id': self.id,
            'local_id': self.local_id,
        }
        self.periods = []

    def get_real_id(self, local_id):
        """
        Given a local index between 0 and the total number of deputies, returns the id of a deputy.
        :return: Returns the id of the deputy, used in the deputies chamber.
        """
        try:
            response = requests.get(OpenDataAPI.current_deputies)
            soup = BeautifulSoup(response.content, 'xml')
            deputies = soup.find_all('Diputado')
            deputy = deputies[local_id]
            real_id = int(deputy.find('DIPID').get_text())
            return real_id
        except Exception as e:
            logger.error(f"Error getting real index: {e}")
            return 0

    def get_profile(self):
        logger.info(f"getting profile for deputy {self.id} ({self.local_id})")
        response = requests.get(self.profile_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        title = soup.find('h2')
        title_text_list = title.getText().strip().split(' ')
        self.profile['name'] = title_text_list[1]
        self.profile['father_surname'] = title_text_list[2]
        self.profile['mother_surname'] = title_text_list[3]

        biography_section = soup.find('div', attrs={'class': 'biografia'})

        profession = 'Sin Información'
        for paragraph in biography_section.findAll('p'):
            if 'Profesion/Actividad' not in paragraph.getText():
                continue
            try:
                profession = paragraph.getText().split('▪')[1].strip()
            except:
                logger.error(f"Error parsing profession: {e}")

        self.profile['profession'] = profession.strip('.')

        general_section = soup.find('section', attrs={'id': 'info-ficha'})

        main_info = general_section.find('div', attrs={'class': 'grid-3'}).getText().strip()
        main_info_list = list(map(str.strip, main_info.split('\r\n')))

        self.profile['district_number'] = int(main_info_list[1].split(':')[1].strip().replace('Nº ', ''))   
        self.profile['district_region'] = main_info_list[2].split(':')[1].strip()
        self.profile['district_communes'] = main_info_list[0].split(':')[1].strip().replace(' ,', ',')
        self.profile['party_name'] = main_info_list[4].split(':')[1].strip()
    
        raw_periods = general_section.findAll('div', attrs={'class': 'grid-2 aleft m-left14'})[-1].findAll('li')[1:]
        parlamentary_periods = list(map(BeautifulSoup.getText, raw_periods))
        self.periods = list(
            map(
                lambda x: {
                    'deputy_id': self.id,
                    'start_date': int(x.split('-')[0]),
                    'end_date': int(x.split('-')[1])
                },
                parlamentary_periods
            )
        )

        contact_info = general_section.findAll('a')
        twitter_info = list(filter(lambda x: 'twitter.com' in x['href'].lower() or 'x.com' in x['href'].lower(), contact_info))
        instagram_info = list(filter(lambda x: 'instagram.com' in x['href'].lower(), contact_info))
        twitter_username = twitter_info[0]['href'].split('/')[-1].strip().replace('@','').replace('Twitter.com','') if len(twitter_info) > 0 else ''
        instagram_username = instagram_info[0]['href'].split('/')[-1].strip() if len(instagram_info) > 0 else ''

        self.profile['twitter_usr'] = twitter_username if twitter_username.lower() != 'no' else ''
        self.profile['instagram_usr'] = instagram_username if instagram_username.lower() != 'no' else ''

        response_xml = requests.get(f'{OpenDataAPI.deputy_data}?prmDiputadoId={self.id}')
        xml_soup = BeautifulSoup(response_xml.content, 'xml')

        raw_birthdate = datetime.strptime(
            xml_soup.find('FechaNacimiento').get_text(),
            '%Y-%m-%dT%H:%M:%S'
        )
        self.profile['birth_date'] = datetime.strftime(raw_birthdate, '%Y-%m-%d')
        self.profile['gender'] = 'MALE' if xml_soup.find('Sexo')['Valor'] == '1' else 'FEMALE'
        militancy_section = xml_soup.find('Militancia')
        self.profile['party_name'] = militancy_section.find('Nombre').getText()
        self.profile['party_acronym'] = militancy_section.find('Alias').getText()
        
    def save_profile(self):
        deputy = Deputy(**self.profile)
        Deputy.save_or_update(deputy)
        periods = list(map(lambda x: DeputyPeriod(**x), self.periods))
        for period in periods:
            DeputyPeriod.save_or_update(period)