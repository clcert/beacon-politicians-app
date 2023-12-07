from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

from io import BytesIO
import requests
import os

APP_RED = (213,28,25)
APP_BLUE = (17,34,51)
APP_WHITE = (255,255,255)

FONT_THIN_PATH = "./OpenSans-Light.ttf"
FONT_REGULAR_PATH = "./OpenSans-Regular.ttf"
FONT_BOLD_PATH = "./OpenSans-Bold.ttf"

TEMPLATE_PATH = os.path.dirname(os.path.abspath(__file__)) + "/template.png"

font_xs = ImageFont.truetype("./OpenSans-Light.ttf", 24)
font_s = ImageFont.truetype("./OpenSans-Light.ttf", 32)
font_m = ImageFont.truetype("./OpenSans-Regular.ttf", 36)
font_m_bold = ImageFont.truetype("./OpenSans-Bold.ttf", 36)
font_ml_bold = ImageFont.truetype("./OpenSans-Bold.ttf", 42)
font_l = ImageFont.truetype("./OpenSans-Bold.ttf", 48)
font_xl = ImageFont.truetype("./OpenSans-Bold.ttf", 60)

class DeputiesPost:
    def __init__(self, name, party, district, picture_url, communes, attendance_percentage, expenses, proposed_law_projects, published_law_projects, pulse):
        self.deputy_name = name
        self.deputy_party = party
        self.deputy_district = district
        self.deputy_picture_url = picture_url
        self.attendance_percentage = attendance_percentage
        self.expenses = expenses
        self.proposed_law_projects = proposed_law_projects
        self.published_law_projects = published_law_projects
        self.pulse = pulse

        self.communes = []
        communes_list = communes.split(",")
        text_length = 0
        content = ""
        for commune in communes_list:
            commune = commune.strip()
            text_length += len(commune) + 2
            if text_length < 50:
                content += f"{commune}, "
            else:
                self.communes.append(content)
                content = f"{commune}, "
                text_length = len(content)
        if content != "" and content not in self.communes:
            self.communes.append(content)

        self.communes[-1] = self.communes[-1][:-2]+"."

        self.template_img = Image.open(TEMPLATE_PATH)
        self.draw = ImageDraw.Draw(self.template_img)

    def write_text(self, text, x, y, font_size=font_m, font_color=APP_BLUE):
        self.draw.text((x, y), text, font_color, font=font_size)

    def paste_image(self, image_url, x, y, width=300, height=300):
        deputy_photo_response = requests.get(image_url)
        deputy_img = Image.open(BytesIO(deputy_photo_response.content))
        deputy_img = deputy_img.resize((width, height))
        self.template_img.paste(deputy_img, (x, y))

    def generate_post(self):
        self.paste_image(self.deputy_picture_url, 82, 252)

        self.write_text("La diputada del día es:", 420, 245, font_size=font_s)
        self.write_text(self.deputy_name, 420, 280, font_size=font_l, font_color=APP_RED)

        self.write_text(f"Diputada por el {self.deputy_district}", 420, 360, font_size=font_s)
        for i in range(len(self.communes)):
            self.write_text(self.communes[i], 420, 405 + i * 35, font_size=font_xs)

        self.write_text(self.deputy_party, 420, 500)

        self.write_text(f"Asistencia", 130, 730, font_size=font_ml_bold, font_color=APP_WHITE)
        self.write_text(f"{self.attendance_percentage}%".replace('.',','), 140, 780, font_size=font_xl, font_color=APP_WHITE)

        self.write_text(f"Gastos", 470, 700, font_size=font_m_bold, font_color=APP_WHITE)
        self.write_text(f"Operacionales", 400, 740, font_size=font_m_bold, font_color=APP_WHITE)
        self.write_text(f"${self.expenses:,}".replace(',','.'), 405, 790, font_size=font_ml_bold, font_color=APP_WHITE)

        self.write_text(f"Proyectos", 740, 700, font_size=font_m_bold, font_color=APP_WHITE)
        self.write_text(f"de Ley", 760, 740, font_size=font_m_bold, font_color=APP_WHITE)
        self.write_text(f"{self.proposed_law_projects} propuestos", 710, 790, font_size=font_m_bold, font_color=APP_WHITE)
        self.write_text(f"{self.published_law_projects} publicados", 720, 835, font_size=font_m_bold, font_color=APP_WHITE)

        self.write_text(f"Pulso de Aleatoriedad: {self.pulse}", 340, 1030, font_size=font_s, font_color=APP_WHITE)

        

        self.template_img.save('todays_deputy.png')

if __name__ == "__main__":
    post = DeputiesPost(
        "Pamela Jiles Moreno", 
        "Partido Humanista", 
        "Distrito 12", 
        "https://www.camara.cl/img.aspx?prmID=GRCL1039",
        "La Florida, La Pintana, Pirque, Puente Alto, San José de Maipo"
    )
    post.generate_post()