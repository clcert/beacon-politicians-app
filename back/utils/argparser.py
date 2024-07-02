from argparse import ArgumentParser, ArgumentTypeError
from datetime import datetime

class CustomParser(ArgumentParser):
    def __init__(self, *args, **kwargs):
        if not kwargs.get("description"):
            kwargs["description"] = (
                "Obtiene la información del diputado del día"
            )
        super().__init__(*args, **kwargs)
        self.add_custom_args()
    
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
        self.add_argument(
            "-l",
            "--load_from_db",
            help="Obtiene el diputado del día indicado y lo actualiza en la base de datos.",
            action="store_true"
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