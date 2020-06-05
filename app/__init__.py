from flask import Flask
from app.factory import appearance
from app.factory import database
from app.factory import views


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.DevelopmentConfig")
    appearance.init_app(app)
    database.init_app(app)
    views.init_app(app)
    return app
