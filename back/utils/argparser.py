from argparse import ArgumentParser, ArgumentTypeError
from datetime import datetime

class CustomArgParser(ArgumentParser):
    def __init__(self, *args, **kwargs):
        if not kwargs.get("description"):
            kwargs["description"] = (
                "Obtiene la información del diputado del día"
            )
        super().__init__(*args, **kwargs)
        self.add_custom_args()

    def add_custom_args(self):
        self.add_argument(
            "-h",
            "--help",
            help="Muestra la ayuda de este comando.",
        )

class SelectorArgParser(CustomArgParser):
    def add_custom_args(self):
        self.add_argument(
            "-d",
            "--date",
            help=(
                "Establece la fecha para obtener el registro que permitirá escoger al diputado, "
                "si no se especifica una hora se asume por defecto las 00:00hrs (zona horaria de Santiago de Chile)."
                "Formato dd/mm/YYYY"
            ),
            type=valid_date
        )
class UpdaterArgParser(CustomArgParser):
    def add_custom_args(self):
        self.add_argument(
            "-p",
            "--update_profile",
            help="Actualiza el perfil del diputado.",
            action="store_true"
        )
        self.add_argument(
            "-a",
            "--update_activity",
            help="Actualiza la actividad del diputado.",
            action="store_true"
        )
        self.add_argument(
            "-t",
            "--update_attendance",
            help="Actualiza la asistencia del diputado.",
            action="store_true"
        )
        self.add_argument(
            "-v",
            "--update_votings",
            help="Actualiza las votaciones del diputado.",
            action="store_true"
        )
        self.add_argument(
            "-e",
            "--update_expenses",
            help="Actualiza los gastos del diputado.",
            action="store_true"
        )
        self.add_argument(
            "-r",
            "--deputies_range",
            help="Establece el rango índices de diputados a actualizar. " + \
                "Formato: <from> <to>, con 0 <= <from> <= <to> <= 154.",
            nargs=2,
            type=valid_deputy_index,
            default=None
        )
        self.add_argument(
            "-d",
            "--deputy_index",
            help="Establece el índice del diputado a actualizar. " + \
                "Formato: 0 <= <index> <= 154.",
            type=valid_deputy_index,
            default=None
        )


def valid_date(date):
    """
    Checks if a date is valid according to the argument parser.
    :param date: String representing a date. Format must be dd-mm-YYYY.
    :return: Datetime object representing the given string.
    """
    try:
        return datetime.strptime(date, "%d/%m/%Y")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(date)
        raise ArgumentTypeError(msg)
    
def valid_deputy_index(value):
    try:
        int_value = int(value)
        if int_value < 0 or int_value > 154:
            raise ValueError
        return int_value
    except ValueError:
        msg = f"Indice de diputado no válido: '{value}'. Debe ser un número entre 0 y 154."
        raise ArgumentTypeError(msg)

