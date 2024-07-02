class OpenDataAPI:
    main_url = "https://opendata.camara.cl/wscamaradiputados.asmx"
    current_deputies = f"{main_url}/getDiputados_Vigentes"
    current_legislature = f"{main_url}/getLegislaturaActual"

class CamaraCL:
    main_url = "https://www.camara.cl/"
    biography = f"{main_url}/diputados/detalle/biografia.aspx"
    operational_expenses = f"{main_url}/diputados/detalle/gastosoperacionales.aspx"
    staff_expenses = f"{main_url}/transparencia/personalapoyogral.aspx"