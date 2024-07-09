from collectors.access_points import OpenDataAPI
from models.models import Attendance
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class AttendanceCollector:
    def __init__(self, deputy_id):
        self.deputy_id = deputy_id

    def get_current_legislature(self):
        """
        Obtains the information from the latest legislature.
        :return: Returns a dictionary containing the id of the latest legislature, and the date of end and start
            as a datetime object.
        """
        logger.info("getting current legislature")
        response = requests.get(OpenDataAPI.current_legislature)
        soup = BeautifulSoup(response.content, 'xml')

        legislature_id = int(soup.find('Id').get_text().strip())

        start = soup.find('FechaInicio').get_text()
        start = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")

        end = soup.find('FechaTermino').get_text()
        end = datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")

        legislature = dict(id=legislature_id, start=start, end=end)

        return legislature


    def get_camera_sessions_id(self, legislature_id=None):
        """
        Obtains a list containing the id for every session of the deputies chamber.
        :return: A list of integers, where each one represents the session id.
        """
        logger.info("getting camera sessions")
        if not legislature_id:
            legislature_id = self.get_current_legislature()['id']

        url = "{}?prmLegislaturaId={}".format(
            OpenDataAPI.sessions_in_legislature, 
            legislature_id
        )
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

        logger.info(f"{len(ids_sessions)} camera sessions obtained")

        return ids_sessions

    def get_justifications(self):
        """
        Obtains a list of all possible justifications for non-attendance.
        :return: Returns a list containing dictionaries objects, where every dictionary contains the information for
        a time of attendance value, as name, reduction of days and the value (the id according to the site).
        """
        response = requests.get(OpenDataAPI.attendance_justifications)
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

    def get_attendance(self):
        """
        Method used to get the attendance of a deputy for all the chamber sessions of the
        current legislature.
        :param deputy_id: Integer representing the deputy id.
        :return: Returns a dictionary containing the number of days attended, unattended justified or not, the total
        number of days and the official percentage of attended days.
        """
        logger.info(f"getting attendance for deputy {self.deputy_id}")
        justifications = self.get_justifications()
        sessions = self.get_camera_sessions_id()

        deputy_attendance = dict(present=0, justified_absent=0, unjustified_absent=0, total=0)

        for session in sessions:
            session_url = f"{OpenDataAPI.attendance_in_session}?prmSesionId={session}"
            response = requests.get(session_url)
            soup = BeautifulSoup(response.content, 'xml')

            # If there is no register of attendance we skip this session
            if not soup.find('Asistencia'):
                continue

            # Only check attendance of the deputy we are looking for
            attendance = list(filter(
                lambda attendance: int(attendance.find('Id').get_text()) == self.deputy_id,
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
        self.deputy_attendance = deputy_attendance
        logger.info(f"attendance for deputy {self.deputy_id} obtained")


    def save_attendance(self):
        """
        Saves the attendance of a deputy in the database.
        """
        attendance = Attendance(
            deputy_id=self.deputy_id,
            total_sessions=self.deputy_attendance['total'],
            total_attended=self.deputy_attendance['present'],
            total_justified=self.deputy_attendance['justified_absent'],
            total_unjustified=self.deputy_attendance['unjustified_absent']
        )
        attendance.save_or_update()