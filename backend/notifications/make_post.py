from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

from io import BytesIO
from datetime import datetime
import requests
import os

APP_RED = (213,28,25)
APP_BLUE = (17,34,51)
APP_WHITE = (255,255,255)

FONT_LIGHT_PATH = "./OpenSans-Light.ttf"
FONT_REGULAR_PATH = "./OpenSans-Regular.ttf"
FONT_BOLD_PATH = "./OpenSans-Bold.ttf"

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = f"{CURRENT_PATH}/template.png"

class BoldFonts:
    XS = ImageFont.truetype(FONT_BOLD_PATH, 24)
    S = ImageFont.truetype(FONT_BOLD_PATH, 32)
    M = ImageFont.truetype(FONT_BOLD_PATH, 36)
    L = ImageFont.truetype(FONT_BOLD_PATH, 42)
    XL = ImageFont.truetype(FONT_BOLD_PATH, 48)
    XXL = ImageFont.truetype(FONT_BOLD_PATH, 60)

class RegularFonts:
    XS = ImageFont.truetype(FONT_REGULAR_PATH, 24)
    S = ImageFont.truetype(FONT_REGULAR_PATH, 32)
    M = ImageFont.truetype(FONT_REGULAR_PATH, 36)
    L = ImageFont.truetype(FONT_REGULAR_PATH, 42)
    XL = ImageFont.truetype(FONT_REGULAR_PATH, 48)
    XXL = ImageFont.truetype(FONT_REGULAR_PATH, 60)

class LightFonts:
    XS = ImageFont.truetype(FONT_LIGHT_PATH, 24)
    S = ImageFont.truetype(FONT_LIGHT_PATH, 32)
    M = ImageFont.truetype(FONT_LIGHT_PATH, 36)
    L = ImageFont.truetype(FONT_LIGHT_PATH, 42)
    XL = ImageFont.truetype(FONT_LIGHT_PATH, 48)
    XXL = ImageFont.truetype(FONT_LIGHT_PATH, 60)


class DeputiesPost:
    def __init__(self, name, gender, date, party, district, picture_url, communes, attendance_percentage, expenses, ranking, proposed_law_projects, published_law_projects, pulse):
        self.deputy_name = name
        self.date = date
        self.deputy_gender = gender
        self.deputy_party = party
        self.deputy_district = district
        self.deputy_picture_url = picture_url
        self.attendance_percentage = attendance_percentage
        self.expenses = expenses
        self.expenses_ranking = ranking
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
            if text_length < 60:
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

    def write_text(self, text, x, y, font_size=RegularFonts.M, font_color=APP_BLUE):
        self.draw.text((x, y), text, font_color, font=font_size)

    def paste_image(self, image_url, x, y, width=300, height=300):
        deputy_photo_response = requests.get(image_url)
        deputy_img = Image.open(BytesIO(deputy_photo_response.content))
        deputy_img = deputy_img.resize((width, height))
        self.template_img.paste(deputy_img, (x, y))

    def generate_post(self):
        self.paste_image(self.deputy_picture_url, 82, 252)

        announcement = "El diputado del día" if self.deputy_gender == "MALE" else "La diputada del día"
        announcement += f" {self.date} es:"
        self.write_text(announcement, 420, 245, font_size=RegularFonts.S)
        self.write_text(self.deputy_name, 420, 280, font_size=BoldFonts.XL, font_color=APP_RED)
        self.write_text(self.deputy_party, 420, 340, font_size=BoldFonts.M)

        deputy_title = "Diputado" if self.deputy_gender == "MALE" else "Diputada"
        charge_text = "Diputado por el " if self.deputy_gender == "MALE" else "Diputada por el "
        charge_text += self.deputy_district
        self.write_text(charge_text, 420, 400, font_size=BoldFonts.S)
        for i in range(len(self.communes)):
            self.write_text(self.communes[i], 420, 445 + i * 35, font_size=RegularFonts.XS)


        self.write_text(f"Asistencia", 115, 710, font_size=BoldFonts.L, font_color=APP_WHITE)
        self.write_text(f"{self.attendance_percentage}%".replace('.',','), 120, 760, font_size=RegularFonts.XXL, font_color=APP_WHITE)

        self.write_text(f"Gastos", 475, 680, font_size=BoldFonts.M, font_color=APP_WHITE)
        self.write_text(f"Operacionales", 405, 720, font_size=BoldFonts.M, font_color=APP_WHITE)
        self.write_text(f"${self.expenses:,}".replace(',','.'), 425, 770, font_size=RegularFonts.L, font_color=APP_WHITE)

        if self.expenses_ranking < 10:
            place_x = 445
            text_x = 500
        elif self.expenses_ranking < 100:
            place_x = 435
            text_x = 510
        else:
            place_x = 425
            text_x = 520
        
        self.write_text(f"{self.expenses_ranking}°", place_x, 845, font_size=BoldFonts.L, font_color=APP_WHITE)
        self.write_text(f"Dip. que", text_x, 845, font_size=RegularFonts.XS, font_color=APP_WHITE)
        self.write_text(f"más gasta", text_x, 875, font_size=RegularFonts.XS, font_color=APP_WHITE)

        self.write_text(f"Proyectos", 760, 700, font_size=BoldFonts.M, font_color=APP_WHITE)
        self.write_text(f"de Ley", 790, 740, font_size=BoldFonts.M, font_color=APP_WHITE)
        self.write_text(f"{self.proposed_law_projects} propuestos", 730, 790, font_size=RegularFonts.M, font_color=APP_WHITE)
        self.write_text(f"{self.published_law_projects} publicados", 740, 835, font_size=RegularFonts.M, font_color=APP_WHITE)

        self.write_text(f"Pulso de Aleatoriedad: {self.pulse}", 340, 1030, font_size=LightFonts.S, font_color=APP_WHITE)

        current_date = datetime.now().strftime("%Y%m%d")
        POST_PATH = f"{CURRENT_PATH}/post{current_date}.png"
        self.template_img.save(POST_PATH)

if __name__ == "__main__":
    post = DeputiesPost(
        "Pamela Jiles Moreno", 
        "Partido Humanista", 
        "Distrito 12", 
        "https://www.camara.cl/img.aspx?prmID=GRCL1039",
        "La Florida, La Pintana, Pirque, Puente Alto, San José de Maipo"
    )
    post.generate_post()