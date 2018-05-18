from flask import Flask
from flask import render_template
from deputy import Deputy

app = Flask(__name__)


@app.route('/', methods=['GET'])
def main_page():
    d = Deputy()
    current = d.info
    return render_template('index.html', **current)


if __name__ == '__main__':
    app.run()
