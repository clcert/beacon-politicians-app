class OpenDataAPI:
    main_url = "https://opendata.camara.cl"

    # Camara diputados ws
    wschamber = f"{main_url}/wscamaradiputados.asmx"
    current_deputies = f"{wschamber}/getDiputados_Vigentes"
    current_legislature = f"{wschamber}/getLegislaturaActual"

    # Diputado ws
    wsdeputy = f"{main_url}/camaradiputados/WServices/WSDiputado.asmx"
    deputy_data = f"{wsdeputy}/retornarDiputado"

class CamaraCL:
    main_url = "https://www.camara.cl/"
    biography = f"{main_url}/diputados/detalle/biografia.aspx"
    operational_expenses = f"{main_url}/diputados/detalle/gastosoperacionales.aspx"
    staff_expenses = f"{main_url}/transparencia/personalapoyogral.aspx"