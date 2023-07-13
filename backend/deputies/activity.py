from utils.drivers import get_driver
from time import sleep

# Selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

MONTH_TRANSLATE = {
    "Ene": "01",
    "Feb": "02",
    "Mar": "03",
    "Abr": "04",
    "May": "05",
    "Jun": "06",
    "Jul": "07",
    "Ago": "07",
    "Sep": "09",
    "Oct": "10",
    "Nov": "11",
    "Dic": "12"
}

class ActivityParser:

    def __init__(self, deputy_id, driver=None):
        self.url = "https://www.camara.cl/legislacion/ProyectosDeLey/proyectos_ley.aspx"
        self.driver = driver if driver else get_driver()
        self.deputy_id = deputy_id

        self.type_selector_id = "ContentPlaceHolder1_ContentPlaceHolder1_ddlTipo"
        self.deputy_selector_id = "ContentPlaceHolder1_ContentPlaceHolder1_ddlAutor"
        self.datepicker_from_id = "ContentPlaceHolder1_ContentPlaceHolder1_fecha_desde"
        self.datepicker_to_id = "ContentPlaceHolder1_ContentPlaceHolder1_fecha_hasta"
        self.search_button_id = "ContentPlaceHolder1_ContentPlaceHolder1_btnBuscar"
        self.change_page_button_id = "ContentPlaceHolder1_ContentPlaceHolder1_pager_rptPager_page_"

        self.project_class = "proyecto"

        self.datepicker_format = "%d/%m/%Y"

    def get_deputy_activity(self, from_date=None, to_date=None):
        self.driver.get(self.url)
        list_of_projects = []

        deputy_selector = Select(self.driver.find_element(By.ID, self.deputy_selector_id))
        deputy_selector.select_by_value(str(self.deputy_id))

        type_selector = Select(self.driver.find_element(By.ID, self.type_selector_id))
        type_selector.select_by_visible_text("Moción") # Set corresponding type

        if from_date:
            datepicker_from = self.driver.find_element(By.ID, self.datepicker_from_id)
            datepicker_from.clear()
            datepicker_from.send_keys(from_date.strftime(self.datepicker_format))

        if to_date:
            datepicker_to = self.driver.find_element(By.ID, self.datepicker_to_id)
            datepicker_to.clear()
            datepicker_to.send_keys(to_date.strftime(self.datepicker_format))

        # Search for projects
        search_button = self.driver.find_element(By.ID, self.search_button_id)
        search_button.click()
        sleep(2) # wait for page to load
        
        # Get the first page of projects
        list_of_projects += self.get_projects_from_page()

        # Now get the rest of the pages
        page = 1
        while True:
            try:
                page_button = self.driver.find_element(By.ID, self.change_page_button_id + str(page))
                page_button.click()
                sleep(2) # wait for page to load
                list_of_projects += self.get_projects_from_page()
                page += 1
            except:
                break
        
        return list_of_projects


    def get_projects_from_page(self):
        projects_in_page = self.driver.find_elements(By.CLASS_NAME, self.project_class)
        law_projects = []

        for project in projects_in_page:
            project_text_lines = project.text.split("\n")
            project_date_split = project_text_lines[4].split(" ")[:3]
            project_date_split[1] = MONTH_TRANSLATE[project_date_split[1].strip(".")]
            project_date = "-".join(project_date_split)
            law_project = {
                "project_id": project_text_lines[0],
                "project_name": project_text_lines[3],
                "project_date": project_date,
                "project_status": project_text_lines[6]
            }
            law_projects.append(law_project)
        return law_projects

        
