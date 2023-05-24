from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap5
from sqlalchemy import MetaData

naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
cors = CORS()
bootstrap = Bootstrap5()
migrate = Migrate()


def init_exts(app):
    db.init_app(app)
    migrate.init_app(app=app, db=db, render_as_batch=True)
    cors.init_app(app)
    bootstrap.init_app(app)
