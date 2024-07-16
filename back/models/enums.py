from enum import Enum
from dataclasses import dataclass

@dataclass
class ErrorMixin:
    code: int
    description: str

class ErrorType(ErrorMixin, Enum):
    REAL_INDEX_ERROR = (1, "Error al obtener el id de la diputada o del diputado desde el servicio OpenData.")
    PROFILE_HTML_ERROR = (2, "Error al obtener datos del diputado desde el perfil en CamaraCL.")
    PROFILE_XML_ERROR = (3, "Error al obtener datos del diputado desde el servicio OpenData.")
    ATTENDANCE_ERROR = (4, "Error al obtener datos de asistencia del diputado desde el servicio OpenData.")
    LEGISLATURE_VOTING_ERROR = (5, "Error al obtener las votaciones en sala de la legislatura actual")
    