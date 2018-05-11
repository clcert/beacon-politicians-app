from flask import Flask
from flask import render_template
import parser.deputies

app = Flask(__name__)


@app.route('/')
def main_page():
    title = 'Politico de semana'
    personalinfo = "Partido por la Procastinación"
    deputy = "Diputado Pedro Gómez"
    intro = "Pedro Gómez, nacido 1 de septiempre de 1949, Abogado de profesión y actualmente diputado por la "
    intro += "5a circunscripción de rancagua"

    return render_template('index.html', title=title, personalinfo=personalinfo, deputy=deputy, intro=intro)


if __name__ == '__main__':
    app.run()
