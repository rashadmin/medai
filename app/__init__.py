from flask import Flask
from config import Config 
from flask_migrate import Migrate
import os                                     
from flask_login import LoginManager
import logging
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

    engine = sa.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    inspector = sa.inspect(engine)
    if not inspector.has_table("user"):
        with app.app_context():
            db.drop_all()
            db.create_all()
            app.logger.info('Initialized the database!')
    return app
from app import models
        