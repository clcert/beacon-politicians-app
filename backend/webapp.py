#######################################################################################################################
# Python 3.5 o superior
# otros requerimientos en requirents.txt
#######################################################################################################################
from flask import Flask, jsonify, abort
from flask_cors import CORS

from deputies.utils import get_sorted_deputies

app = Flask(__name__)
CORS(app)


@app.route('/api/diputadodeldia')
def main_page():
    deputies_list = get_sorted_deputies()
    if len(deputies_list) == 0:
        abort(404)
        return
    last_deputy = deputies_list[-1]
    return jsonify(last_deputy)


@app.route('/api/diputados')
def all_deputies():
    deputies_list = get_sorted_deputies()
    if len(deputies_list) == 0:
        abort(404)
        return
    return jsonify(deputies_list)


@app.route('/api/diputado/date/<string:selection_date>')
def dateRecord(selection_date):
    deputies_list = get_sorted_deputies()
    deputy = list(filter(lambda d: d['date'].split(' ')[0] == selection_date, deputies_list))
    if len(deputy) == 0:
        abort(404)
        return
    return jsonify(deputy[0])


@app.route('/api/dates')
def dates():
    deputies_list = get_sorted_deputies()
    dates = list(map(lambda x: x['date'], deputies_list))
    dates.sort()
    return jsonify({'dates': dates})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
