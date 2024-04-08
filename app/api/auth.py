from flask import jsonify,abort
from app.models import User,Conversation,Anonyuser
from app.api.errors import error_response
from app import db
from app.api import bp
from flask_httpauth import HTTPBasicAuth,HTTPTokenAuth
basic_auth = HTTPBasicAuth()

@basic_auth.verify_password
def verify_password(username,password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user
@basic_auth.error_handler 
def basic_auth_error(status):
    return error_response(status)

