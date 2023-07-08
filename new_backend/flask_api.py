from flask import Flask, jsonify, abort
from flask_cors import CORS

from utils.utils import get_json_data

app = Flask(__name__)
CORS(app)

def get_sort_by_date_deputies():
    """
    Returns an ordered dictionary of deputies sorted by date.
    :return:
    """
    json_data = get_json_data()
    deputies = json_data['records']
    record_dates = list(deputies.keys())
    record_dates.sort()
    sorted_dict = {i: deputies[i] for i in record_dates}
    return sorted_dict


@app.route('/api/diputados/last')
def last_deputy():
    deputies = get_sort_by_date_deputies()
    if not deputies:
        abort(404)
    last_deputy = list(deputies.values())[-1]
    return jsonify(last_deputy)


@app.route('/api/diputados')
def all_deputies():
    deputies = get_sort_by_date_deputies()
    if not deputies:
        abort(404)
    return jsonify(deputies)


@app.route('/api/diputados/archivo/<string:selection_date>')
def dateRecord(selection_date):
    deputies = get_sort_by_date_deputies()
    try:
        deputy = deputies[selection_date]
        return jsonify(deputy)
    except KeyError:
        abort(404)


@app.route('/api/fechas')
def dates():
    deputies_dates = list(get_sort_by_date_deputies().keys())
    return jsonify({'dates': deputies_dates})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
