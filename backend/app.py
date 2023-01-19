#######################################################################################################################
# Python 3.5 o superior
# otros requerimientos en requirents.txt
#######################################################################################################################
from flask import Flask, jsonify
from flask import abort
from deputy import Deputy
from updater import Updater
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.route('/api/diputadodeldia')
def main_page():
    deputies_list = Updater().get_list()
    if len(deputies_list) == 0:
        abort(404)
        return
    last_deputy = Updater().get_list()[0]
    return jsonify(last_deputy)


@app.route('/api/diputado/date/<string:selection_date>')
def dateRecord(selection_date):
    deputies_list = Updater().get_list()
    deputy = list(filter(lambda d: d['date'].split(' ')[0] == selection_date, deputies_list))
    if len(deputy) == 0:
        abort(404)
        return
    d = Deputy(int(deputy[0]['index']))
    current = d.info
    return jsonify(current)


@app.route('/api/dates')
def dates():
    deputies_list = Updater().get_list()
    dates = list(map(lambda x: x['date'], deputies_list))
    dates.sort()
    return jsonify({'dates': dates})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
