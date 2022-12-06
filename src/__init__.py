from os import urandom
from flask import Flask


def create_app():
    """
    flask app creation function
    :return: Flask app
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = urandom(24)

    from src.views import views

    app.register_blueprint(views, url_prefix='/')

    return app
