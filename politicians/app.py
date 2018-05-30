from flask import Flask
from flask import render_template
from flask import abort
from deputy import Deputy
from updater import Updater

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main_page():
    last = len(Updater().get_list()) - 1
    d = Deputy(last)
    current = d.info
    return render_template('index.html', **current)


@app.route('/diputado/<int:json_index>')
def record(json_index):
    last = len(Updater().get_list()) - 1
    if json_index < 0 or json_index > last:
        abort(404)
        return
    d = Deputy(json_index)
    current = d.info
    return render_template('index.html', **current)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
