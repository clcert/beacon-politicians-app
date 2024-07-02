from collectors.expenses.expenses import ExpensesCollector
from collectors.access_points import CamaraCL

class OperationalExpensesCollector(ExpensesCollector):
    def __init__(self, profile, **kwargs):
        super().__init__(**kwargs)
        deputy_id = profile['id']
        self.url = f'{CamaraCL.operational_expenses}?prmId={deputy_id}'
        self.month_selector_id = 'ContentPlaceHolder1_ContentPlaceHolder1_DetallePlaceHolder_ddlMes'
        self.year_selector_id = 'ContentPlaceHolder1_ContentPlaceHolder1_DetallePlaceHolder_ddlAno'

    def parse_and_filter_table(self, html_table):
        lines = html_table.splitlines()
        expenses = dict()
        expenses['Otros gastos de oficina parlamentaria'] = 0
        expenses['Web y Almacenamiento'] = 0
        expenses['Otros'] = 0
        total = 0
        for line in lines[1:]:
            [title, amount] = line.split('   ')
            title = title.replace('(**monto ajustado por nota de crédito recibida)','').strip()
            integer_amount = int(amount.strip().replace('.', ''))
            total += integer_amount
            if title in OP_EXPENSES_OFFICE:
                expenses['Otros gastos de oficina parlamentaria'] += integer_amount
            elif title in OP_EXPENSES_WEB:
                expenses['Web y Almacenamiento'] += integer_amount
            elif title in OP_EXPENSES_OTHERS:
                expenses['Otros'] += integer_amount
            else:
                expenses[title.lower().capitalize()] = integer_amount
        self.expenses = expenses


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