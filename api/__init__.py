from flask import Flask
from config import config


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    return app


app = create_app('development')


from api import models
from api.auth import auth
from api.bucketlist import bucketlist
