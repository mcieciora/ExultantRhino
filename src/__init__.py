from os import urandom
from flask import Flask
from src.views import views


def create_app():
    """
    flask app creation function
    :return: Flask app
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = urandom(24)
    app.register_blueprint(views, url_prefix='/')

    return app
