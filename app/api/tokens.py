from flask import jsonify,abort
from app.models import User,Conversation,Anonyuser
from app.api.errors import error_response
from app import db
from app.api import bp
from flask_httpauth import HTTPTokenAuth
from app.api.auth import basic_auth


token_auth = HTTPTokenAuth()


@bp.route('/token',methods=['POST'])
@basic_auth.login_required
def get_token():
    token = basic_auth.current_user().get_token()
    db.session.commit()
    return jsonify({'token':token})


@bp.route('/token',methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    token_auth.current_user().revoke_token()
    db.session.commit()
    return '',204

@token_auth.verify_token
def verify_token(token):
    return User.check_token(token) if token else None

@token_auth.error_handler
def token_auth_error(status):
    return error_response(status)