import os
from flask import Flask
from app.main import init_app

from extensions import init_exts

base_dir = os.path.abspath(os.path.dirname(__file__))
CSQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(base_dir, "../db", "db_chat.db")


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = CSQLALCHEMY_DATABASE_URI

    init_exts(app)

    init_app(app)

    # with app.app_context():
    #     db.create_all()

    return app
