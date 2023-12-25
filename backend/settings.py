from os.path import dirname, abspath
from dotenv import dotenv_values

"""
GENERAL SETTINGS
"""
CURR_PATH = dirname(abspath(__file__))
PROJECT_DIR = CURR_PATH.replace("/utils", "")
config = dotenv_values(f"{PROJECT_DIR}/.env")

DB_PATH = "{}/{}".format(PROJECT_DIR, config["DB_PATH"])
JSON_PATH = "{}/{}".format(PROJECT_DIR, config["JSON_PATH"])

"""
SOCIAL MEDIA CREDENTIALS
"""
TELEGRAM_TOKEN = config["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = config["TELEGRAM_CHAT_ID"]
DISCORD_WEBHOOK_ID = config["DISCORD_WEBHOOK_ID"]
TWITTER_CONSUMER_KEY = config["TWITTER_CONSUMER_KEY"]
TWITTER_CONSUMER_SECRET = config["TWITTER_CONSUMER_SECRET"]
TWITTER_ACCESS_TOKEN = config["TWITTER_ACCESS_TOKEN"]
TWITTER_ACCESS_TOKEN_SECRET = config["TWITTER_ACCESS_TOKEN_SECRET"]


"""
URLS AND ENDPOINTS
"""
# OpenData Camara main URL
OPENDATA_CAMARA_URL = "http://opendata.camara.cl/camaradiputados/WServices/"

# OpenData Camara API endpoints
CURRENT_DEPUTIES_URL = OPENDATA_CAMARA_URL + "WSDiputado.asmx/retornarDiputadosPeriodoActual"

BASE_SESSIONS_IN_LEGISLATURE_URL = OPENDATA_CAMARA_URL + 'WSSala.asmx/retornarSesionesXLegislatura'
BASE_ATTENDANCES_URL = OPENDATA_CAMARA_URL + 'WSSala.asmx/retornarSesionAsistencia'
JUSTIFICATIONS_URL = OPENDATA_CAMARA_URL + 'WSComun.asmx/retornarTiposJustificacionesInasistencia'


"""
OTHER CONSTANTS
"""
MONTHS = [
    "enero",    "febrero",  "marzo",        "abril",    "mayo",         "junio", 
    "julio",    "agosto",   "septiembre",   "octubre",  "noviembre",    "diciembre",
]

OP_EXPENSES_TYPES = [
    "Otros gastos de oficina parlamentaria",
    "Web y Almacenamiento",
    "Telefonía",
    "Traslación",
    "Difusión",
    "Actividades destinadas a la interacción con la comunidad",
    "Correspondencia",
    "Traspaso desde gastos operacionales a asignación personal de apoyo",
    "Consumos básicos",
    "Seguros de bienes",
    "Arriendo de inmueble",
    "Otros",
]

OP_EXPENSES_OFFICE = [
    "EQUIPAMIENTO OFICINA PARLAMENTARIA",
    "MATERIALES DE OFICINA",
    "GASTOS DE MANTENCIÓN OFICINA PARLAMENTARIA (INMUEBLE)",
    "REPARACIONES LOCATIVAS DEL INMUEBLE",
    "ARRIENDO DE OFICINAS VIRTUALES",
    "ARRIENDO DE OFICINA MÓVIL",
    "MANTENCION Y REPARACIÓN DE OFICINA MÓVIL",
    "HABILITACIÓN DE SEDES PARLAMENTARIAS (CON AUTORIZACIÓN DE CRAP)",
]

OP_EXPENSES_WEB = [
    "SERVICIOS WEB",
    "CONTRATACIÓN SERVICIO DE ALMACENAMIENTO",
]

OP_EXPENSES_OTHERS = [
    "SERVICIOS MENORES",
    "COVID-19 PERSONAL DE APOYO",
]