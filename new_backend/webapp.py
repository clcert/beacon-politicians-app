from flask import Flask, jsonify, abort
from flask_cors import CORS

from utils.utils import get_json_data

app = Flask(__name__)
app.json.sort_keys = False
CORS(app)

def get_sorted_by_date_deputies():
    """
    Returns an ordered dictionary of deputies sorted by date.
    :return:
    """
    json_data = get_json_data()
    deputies = json_data['records']
    deputies.sort(key=lambda dep: dep['date'])
    return deputies


@app.route('/deputies/last')
def last_deputy():
    deputies = get_sorted_by_date_deputies()
    if not deputies:
        abort(404)
    last_deputy = deputies[-1]
    return jsonify(last_deputy)


@app.route('/deputies')
def all_deputies():
    deputies = get_sorted_by_date_deputies()
    if not deputies:
        abort(404)
    return jsonify(deputies)


@app.route('/deputies/archive/<string:selection_date>')
def dateRecord(selection_date):
    deputies = get_sorted_by_date_deputies()
    try:
        deputy = next(dep for dep in deputies if dep['date'] == selection_date)
        return jsonify(deputy)
    except KeyError:
        abort(404)


@app.route('/dates')
def dates():
    deputies = get_sorted_by_date_deputies()
    if not deputies:
        abort(404)
    return jsonify({'dates': [dep['date'] for dep in deputies]})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
