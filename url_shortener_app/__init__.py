from flask import Flask
from . import url_short
import json


def create_app(test_config=None):
    with open('keys.json') as fo:
        key = json.load(fo)

    app = Flask(__name__)
    app.secret_key = key['secret_key']
    app.register_blueprint(url_short.routes.bp, url_prefix='/')
    return app
