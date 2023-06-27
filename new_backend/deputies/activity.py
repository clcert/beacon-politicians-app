from utils.drivers import get_driver

# Selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

class ActivityParser:

    def __init__(self) -> None:
        self.url = "https://www.camara.cl/legislacion/ProyectosDeLey/proyectos_ley.aspx"
        self.driver = get_driver()

        self.deputy_selector_id = "ContentPlaceHolder1_ContentPlaceHolder1_ddlAutor"
        self.datepicker_from_id = "ContentPlaceHolder1_ContentPlaceHolder1_fecha_desde"
        self.datepicker_to_id = "ContentPlaceHolder1_ContentPlaceHolder1_fecha_hasta"
        self.search_button_id = "ContentPlaceHolder1_ContentPlaceHolder1_btnBuscar"
        self.change_page_button_id = "ContentPlaceHolder1_ContentPlaceHolder1_pager_rptPager_page_{}"

        self.project_class = "proyecto"

        self.datepicker_format = "%d/%m/%Y"

    def get_deputy_activity(self, deputy_id, from_date=None, to_date=None):
        self.driver.get(self.url)
        list_of_projects = []

        deputy_selector = Select(self.driver.find_element(By.ID, self.deputy_selector_id))
        deputy_selector.select_by_value(str(deputy_id))

        if from_date:
            datepicker_from = self.driver.find_element(By.ID, self.datepicker_from_id)
            datepicker_from.clear()
            datepicker_from.send_keys(from_date.strftime(self.datepicker_format))

        if to_date:
            datepicker_to = self.driver.find_element(By.ID, self.datepicker_to_id)
            datepicker_to.clear()
            datepicker_to.send_keys(to_date.strftime(self.datepicker_format))

        search_button = self.driver.find_element(By.ID, self.search_button_id)
        search_button.click()
        
        
