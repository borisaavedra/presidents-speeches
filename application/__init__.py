from flask import Flask
import csv
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)

    with app.app_context():
        from . import routes

        app.register_blueprint(routes.main_bp)

        db.create_all()

    return app