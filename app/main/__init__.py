from flask import Blueprint


bp = Blueprint(
    "main",
    __name__,
    template_folder="./templates",
    static_folder="./static",
    static_url_path="/main/static",
)

from .chat import *
from .home import *


def init_app(app):
    app.register_blueprint(bp)
