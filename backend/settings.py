from os import path
from enum import Enum

class JsonFiles(Enum):
    """
    Enum used to identify the json file to be used.
    """
    DEPUTIES = 1
    EXPENSES = 2

FILE_LOCATIONS = {
    JsonFiles.DEPUTIES: path.dirname(path.realpath(__file__)) + '/deputies.json',
    JsonFiles.EXPENSES: path.dirname(path.realpath(__file__)) + '/expenses.json',
}

OPENDATA_CAMARA_URL = 'http://opendata.camara.cl/camaradiputados/WServices/'

CURRENT_DEPUTIES_URL = OPENDATA_CAMARA_URL + 'WSDiputado.asmx/retornarDiputadosPeriodoActual'
JUSTIFICATIONS_URL = OPENDATA_CAMARA_URL + 'WSComun.asmx/retornarTiposJustificacionesInasistencia'

ALL_LEGISLATURES_URL = 'http://opendata.camara.cl/wscamaradiputados.asmx/getLegislaturas'
CURRENT_LEGISLATURE_URL = OPENDATA_CAMARA_URL + 'WSLegislativo.asmx/retornarLegislaturaActual'
BASE_SESSIONS_IN_LEGISLATURE_URL = OPENDATA_CAMARA_URL + 'WSSala.asmx/retornarSesionesXLegislatura?prmLegislaturaId='

BASE_VOTINGS_LEGISLATURE_URL = OPENDATA_CAMARA_URL + 'WSLegislativo.asmx/retornarVotacionesXAnno?prmAnno='
BASE_VOTING_DETAIL_URL = OPENDATA_CAMARA_URL + 'WSLegislativo.asmx/retornarVotacionDetalle?prmVotacionId='
BASE_BULLETIN_LAW_PROJECT_URL = OPENDATA_CAMARA_URL + 'WSLegislativo.asmx/retornarProyectoLey?prmNumeroBoletin='

BASE_PROFILES_URL = 'https://www.camara.cl/diputados/detalle/biografia.aspx?prmId='
BASE_PROFILE_PIC_URL = 'https://www.camara.cl/img.aspx?prmID=GRCL'
BASE_DEPUTY_INFO_URL = OPENDATA_CAMARA_URL + 'WSDiputado.asmx/retornarDiputado?prmDiputadoId='
BASE_ATTENDANCES_URL = OPENDATA_CAMARA_URL + 'WSSala.asmx/retornarSesionAsistencia?prmSesionId='

TOKEN_TELEGRAM_BOT = None
TELEGRAM_CHAT_ID = ''
DISCORD_WEBHOOK_URL = ''

# Voting filter
# Blacklist of keywords
VOTING_BLACKLIST = [
    'modifica',
    'ley',
    'n°',
    'solicita',
    'presidente'
]

MONTHS = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

OP_EXPENSES_TYPES = [
    'Otros gastos de oficina parlamentaria',
    'Web y Almacenamiento',
    'Telefonía',
    'Traslación',
    'Difusión',
    'Actividades destinadas a la interacción con la comunidad',
    'Correspondencia',
    'Traspaso desde gastos operacionales a asignación personal de apoyo',
    'Consumos básicos',
    'Seguros de bienes',
    'Arriendo de inmueble',
    'Otros',
]

OP_EXPENSES_OFFICE = [
    # 'ARRIENDO DE INMUEBLE',
    'EQUIPAMIENTO OFICINA PARLAMENTARIA',
    'MATERIALES DE OFICINA',
    'GASTOS DE MANTENCIÓN OFICINA PARLAMENTARIA (INMUEBLE)',
    'REPARACIONES LOCATIVAS DEL INMUEBLE',
    'ARRIENDO DE OFICINAS VIRTUALES',
    'ARRIENDO DE OFICINA MÓVIL',
    'MANTENCION Y REPARACIÓN DE OFICINA MÓVIL',
    'HABILITACIÓN DE SEDES PARLAMENTARIAS (CON AUTORIZACIÓN DE CRAP)',
]

OP_EXPENSES_WEB = [
    'SERVICIOS WEB',
    'CONTRATACIÓN SERVICIO DE ALMACENAMIENTO',
]

OP_EXPENSES_OTHERS = [
    'SERVICIOS MENORES',
    'COVID-19 PERSONAL DE APOYO',
]