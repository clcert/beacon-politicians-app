from bs4 import BeautifulSoup
import requests

from utils.utils import get_current_legislature
from utils.settings import OPENDATA_CAMARA_URL

BASE_SESSIONS_IN_LEGISLATURE_URL = OPENDATA_CAMARA_URL + 'WSSala.asmx/retornarSesionesXLegislatura?prmLegislaturaId='
BASE_ATTENDANCES_URL = OPENDATA_CAMARA_URL + 'WSSala.asmx/retornarSesionAsistencia?prmSesionId='
JUSTIFICATIONS_URL = OPENDATA_CAMARA_URL + 'WSComun.asmx/retornarTiposJustificacionesInasistencia'

def parse_deputy_attendance(deputy_id):
    """
    Method used to get the attendance of a deputy for all the chamber sessions of the
    current legislature.
    :param deputy_id: Integer representing the deputy id.
    :return: Returns a dictionary containing the number of days attended, unattended justified or not, the total
    number of days and the official percentage of attended days.
    """
    justifications = parse_justifications()
    sessions = get_camera_sessions()

    deputy_attendance = dict(present=0, justified_absent=0, unjustified_absent=0, total=0)

    for session in sessions:
        session_url = BASE_ATTENDANCES_URL + str(session)
        response = requests.get(session_url)
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
            deputy_attendance['present'] += 1

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
                deputy_attendance['justified_absent'] += 1
            else:
                deputy_attendance['unjustified_absent'] += 1

    # Add total number of sessions
    deputy_attendance['total'] = len(sessions)

    return deputy_attendance


def parse_justifications():
    """
    Obtains a list of all possible justifications for non-attendance.
    :return: Returns a list containing dictionaries objects, where every dictionary contains the information for
    a time of attendance value, as name, reduction of days and the value (the id according to the site).
    """
    response = requests.get(JUSTIFICATIONS_URL)
    soup = BeautifulSoup(response.content, 'xml')

    justifications = soup.find_all('JustificacionInasistencia')
    justifications_list = []

    for i in range(len(justifications)):
        justification = dict()
        justification['name'] = justifications[i].find('Nombre').get_text()
        justification['reductionattendance'] = 1 if justifications[i].find('RebajaAsistencia').get_text() == 'true' else 0
        justification['value'] = justifications[i]['Valor']
        justifications_list.append(justification)

    return justifications_list


def get_camera_sessions():
    """
    Obtains a list containing the id for every session of the deputies chamber.
    :return: A list of integers, where each one represents the session id.
    """
    url = BASE_SESSIONS_IN_LEGISLATURE_URL + str(get_current_legislature()['id'])
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'xml')

    sessions = soup.find_all('Sesion')

    # If a session hasn't been celebrated, remove it from the list.
    celebrated_sessions = list(filter(
        lambda session: session.find('Estado')['Valor'] == '1',
        sessions
    ))

    # Gets only session ids from the list.
    ids_sessions = list(map(
        lambda session: int(session.find('Id').get_text().strip()),
        celebrated_sessions
    ))

    return ids_sessions