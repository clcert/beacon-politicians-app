from flask import Flask
from flask import render_template
from deputy import Deputy

app = Flask(__name__)


@app.route('/', methods=['GET'])
def main_page():
    d = Deputy()
    current = d.info['deputy']

    current['modified'] = d.info['modified']
    length = 0
    for i in range(len(current['modified'])):
        if current['modified'][i] == '.':
            length = i
            break
    current['modified'] = current['modified'][0:length]

    return render_template('index.html', **current)


if __name__ == '__main__':
    app.run()
