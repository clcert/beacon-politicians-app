class OpenDataAPI:
    main_url = "https://opendata.camara.cl"

    # Camara diputados ws
    ws_deputies_chamber = f"{main_url}/wscamaradiputados.asmx"

    # Other ws
    ws_chamber = f"{main_url}/camaradiputados/WServices"
    ws_deputy = f"{ws_chamber}/WSDiputado.asmx"
    ws_legislative = f"{ws_chamber}/WSLegislativo.asmx"
    ws_sala = f"{ws_chamber}/WSSala.asmx"
    ws_common = f"{ws_chamber}/WSComun.asmx"

    # Profiles
    current_deputies = f"{ws_deputy}/retornarDiputadosPeriodoActual"
    deputy_data = f"{ws_deputy}/retornarDiputado"

    # Attendance
    current_legislature = f"{ws_legislative}/retornarLegislaturaActual"
    sessions_in_legislature = f"{ws_sala}/retornarSesionesXLegislatura"
    attendance_justifications = f"{ws_common}/retornarTiposJustificacionesInasistencia"
    attendance_in_session = f"{ws_sala}/retornarSesionAsistencia"

class CamaraCL:
    main_url = "https://www.camara.cl/"
    biography = f"{main_url}/diputados/detalle/biografia.aspx"
    operational_expenses = f"{main_url}/diputados/detalle/gastosoperacionales.aspx"
    staff_expenses = f"{main_url}/transparencia/personalapoyogral.aspx"