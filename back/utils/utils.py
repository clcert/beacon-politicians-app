from datetime import datetime

MONTHS = [
    "enero",    "febrero",  "marzo",        "abril",    "mayo",         "junio", 
    "julio",    "agosto",   "septiembre",   "octubre",  "noviembre",    "diciembre",
]

def get_current_month():
    return datetime.now().month

def get_current_year():
    return datetime.now().year