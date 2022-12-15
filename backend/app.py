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
    last = len(Updater().get_list()) - 1
    d = Deputy(last)
    current = d.info
    current['ljson_index'] = last
    return jsonify(current)


@app.route('/api/diputado/<int:json_index>')
def record(json_index):
    last = len(Updater().get_list()) - 1
    if json_index < 0 or json_index > last:
        abort(404)
        return
    d = Deputy(json_index)
    current = d.info
    current['ljson_index'] = last
    return jsonify(current)


@app.route('/api/dates')
def dates():
    deputies_list = Updater().get_list()
    dates = list(map(lambda x: x['date'], deputies_list)).sort()
    return jsonify({'dates': dates})
    

if __name__ == '__main__':
    app.run(host='0.0.0.0')
