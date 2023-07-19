OPENDATA_CAMARA_URL = 'http://opendata.camara.cl/camaradiputados/WServices/'
CURRENT_DEPUTIES_URL = OPENDATA_CAMARA_URL + 'WSDiputado.asmx/retornarDiputadosPeriodoActual'

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

DEPUTIES_JSON_PATH = 'data/last_deputies.json'