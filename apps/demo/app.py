from urllib.parse import urlparse

import dill
import validators
from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request

app = Flask('APP')

with open('data/model.bin', 'rb') as f:
    predictor = dill.load(f)


def predict(url: str):
    if urlparse(url).netloc == '':
        url = 'http://' + url
    return predictor.predict([urlparse(url).netloc])


@app.route('/predict', methods=['POST'])
def predict_handler():
    request_data = request.json
    url = request_data['url']

    if not (validators.domain(url) is True):  # fix type
        return jsonify(None), 400

    return jsonify(predict(url))


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
