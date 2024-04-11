from dotenv import load_dotenv
import os
basedir = os.path.abspath(os.path.dirname(__name__))
#basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ayom0908'
    if os.getenv('DATABASE_URL'):
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL').replace("postgres://", "postgresql://", 1)
    else:
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'app.db')}"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMINS = ['abdul.a.rasheed2022@gmail.com']
    CHAT_PER_PAGE = 5
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    LOG_WITH_GUNICORN = os.getenv('LOG_WITH_GUNICORN', default=False)
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
    