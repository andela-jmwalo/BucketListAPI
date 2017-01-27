from flask import Flask
from config.config import app_config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])

    db.init_app(app)

    from api.auth.auth import auth_view
    app.register_blueprint(auth_view)

    from api.bucketlist.bucketlist import bucket_view
    app.register_blueprint(bucket_view)

    return app
