class OpenDataAPI:
    main_url = "https://opendata.camara.cl/"
    current_deputies = f"{main_url}wscamaradiputados.asmx/getDiputados_Vigentes"

class CamaraCL:
    main_url = "https://www.camara.cl/"
    biography = f"{main_url}/diputados/detalle/biografia.aspx"
    operational_expenses = f"{main_url}/diputados/detalle/gastosoperacionales.aspx"
    staff_expenses = f"{main_url}/transparencia/personalapoyogral.aspx"