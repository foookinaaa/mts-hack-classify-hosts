import os
from urllib.parse import urlparse

import dill
import validators
from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request

MODEL_FILE = os.path.join(os.path.dirname(__file__), 'data/model.bin')
SERVER_PORT = int(os.environ.get('SERVER_PORT', '8080'))

app = Flask('APP')

with open(MODEL_FILE, 'rb') as f:
    predictor = dill.load(f)  # pickle like


def is_valid_domain(url):
    return validators.domain(url) is True  # fix type


def predict(url: str):
    if urlparse(url).netloc == '':  # hotfix host without protocol
        url = 'http://' + url
    return predictor.predict([urlparse(url).netloc])


@app.route('/predict', methods=['POST'])
def predict_handler():
    request_data = request.json
    url = request_data['url']

    if not is_valid_domain(url):
        return jsonify(None), 400

    return jsonify(predict(url))


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=SERVER_PORT)  # single thread server must be replaced with gunicorn
