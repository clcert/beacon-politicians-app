from flask import Flask
from flask import render_template
from deputy import Deputy

app = Flask(__name__)


@app.route('/')
def main_page():
    d = Deputy()
    current = d.info['current']
    current["lastperiod"] = current["periods"][len(current["periods"])-1]
    return render_template('index.html', **current)


if __name__ == '__main__':
    app.run()
