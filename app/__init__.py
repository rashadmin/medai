from flask import Flask
from config import Config 
from flask_migrate import Migrate
import os                                     
from flask_login import LoginManager
import logging
from logging.handlers import RotatingFileHandler
import sqlalchemy as sa
from flask_cors import CORS
from app.extensions import db


migrate = Migrate()
login = LoginManager()
cors =CORS()
login.login_view = 'auth.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app,db)
    login.init_app(app)
    cors.init_app(app)
    with app.app_context():
        from app.api import bp as api_bp
        app.register_blueprint(api_bp,url_prefix='/api')
        from app.chat import bp as chat_bp
        app.register_blueprint(chat_bp)
        from app.videos import bp as videos_bp
        app.register_blueprint(videos_bp)

    engine = sa.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    inspector = sa.inspect(engine)
    if not inspector.has_table("user"):
        with app.app_context():
            db.drop_all()
            db.create_all()
            app.logger.info('Initialized the database!')
    if app.config['LOG_WITH_GUNICORN']:
        gunicorn_error_logger = logging.getLogger('gunicorn.error')
        app.logger.handlers.extend(gunicorn_error_logger.handlers)
        app.logger.setLevel(logging.DEBUG)
    else:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/app.log',maxBytes=10240,backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s : %(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('hub_startup')
    return app
from app import models
        