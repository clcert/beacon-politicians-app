from argparse import ArgumentParser, ArgumentTypeError

class CustomParser(ArgumentParser):
    def __init__(self, *args, **kwargs):
        if not kwargs.get("description"):
            kwargs["description"] = (
                "By default, gets and updates information for the last deputy, or print it. Also, given a date and " \
                "hour in specific, can get information of the deputy that should be obtained by using the correspo" \
                "nding record of that date."
            )
        super().__init__(*args, **kwargs)
        self.add_custom_args()
    
    def add_custom_args(self):
        self.add_argument(
            "-i",
            "--init",
            help="Inicializar la base de datos.",
            action="store_true"
        )
        self.add_argument(
            "--update_profiles",
            help="Actualizar la información básica de los diputados.",
            action="store_true"
        )
        self.add_argument(
            "-u",
            "--update_expenses",
            help="Actualizar la información de gastos de los diputados indicados.",
            type=valid_range,
        )
        self.add_argument(
            "-d",
            "--date",
            help=(
                "Establece la fecha para obtener el registro que permitirá escoger al diputado, "
                "si no se especifica una hora se asume por defecto las 00:00hrs (zona horaria de Santiago de Chile)."
                "Formato dd-mm-YYYY"
            ),
            type=valid_date
        )
        self.add_argument(
            "-t",
            "--time",
            help=(
                "Establece la hora para obtener el registro que permitirá escoger al diputado. "
                "Formato HH:MM"
            ),
            type=valid_time
        )
        self.add_argument(
            "-e",
            "--epoch",
            help=(
                "Sets the date and time to the given epoch. If date or time are given, will prioritize"
                "the epoch argument."
            ),
            type=int
        )
        self.add_argument(
            "-v",
            "--verify",
            help="¿Quieres verificar un resultado? Indícalo con esta opción.",
        )
        
        

def valid_range(range):
    """
    Checks if the given range is valid.
    A range is considered valid if it has the following format:
        <start>-<end>
    Where <start> and <end> are integers and <start> is less than <end>.
    Also, <start> and <end> must be in {1,...,155}.
    """
    try:
        start, end = range.split("-")
        start, end = int(start), int(end)
        if start < 1 or start > 155 or end < 1 or end > 155 or start > end:
            raise ValueError
        return (start-1, end)
    except ValueError:
        msg = "Invalid deputies id range: '{0}'.".format(range)
        raise ArgumentTypeError(msg)


def valid_date(date):
    """
    Checks if a date is valid according to the argument parser.
    :param date: String representing a date. Format must be dd-mm-YYYY.
    :return: Datetime object representing the given string.
    """
    try:
        return datetime.strptime(date, "%d-%m-%Y")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(date)
        raise ArgumentTypeError(msg)


def valid_time(time):
    """
    Checks if an hour is valid according to the argument parser.
    :param hour: String representing an hour. Format must be HH:MM.
    :return: Datetime object representing te given string.
    """
    try:
        return datetime.strptime(time, "%H:%M")
    except ValueError:
        msg = "Not a valid hour: '{0}'.".format(time)
        raise ArgumentTypeError(msg)