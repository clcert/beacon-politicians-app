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


# @app.route('/diputadodeldia/handle_previous', methods=['POST'])
# def handle_previous():
#     json_index = int(request.args['json_index']) - 1
#     return redirect(url_for("record", json_index=json_index))


# @app.route('/diputadodeldia/handle_next', methods=['POST'])
# def handle_next():
#     json_index = int(request.args['json_index']) + 1
#     last = len(Updater().get_list()) - 1
#     if json_index == last:
#         return redirect(url_for("main_page"))
#     else:
#         return redirect(url_for("record", json_index=json_index))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
