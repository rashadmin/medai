from app.api import bp
from flask import jsonify,request,url_for,abort
from app.models import User,Conversation,Anonyuser
from app.api.errors import bad_request
from app import db
from app.api.tokens import token_auth

@bp.route('/users',methods=['POST'])
def create_user():
    data =request.get_json() or {}
    if 'username' not in data or 'email' not in data or 'firstname' not in data or 'lastname' not in data:
        return bad_request('Must include FIRST NAME,LAST_NAME,USERNAME,EMAIL')
    if User.query.filter_by(username=data['username']).first():
        return bad_request(f'Use a different username as {data["username"]} is taken!')
    if User.query.filter_by(email=data['email']).first():
        return bad_request(f'Use a different email as {data["email"]} has been used!')
    user = User()
    print(data)
    user.from_dict(data,new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code=201
    response.headers['location'] = url_for('api.get_user',id=user.id)
    return response

@bp.route('/users/<int:id>',methods=['PUT'])
@token_auth.login_required
def update_user(id):
    if token_auth.current_user().id!=id:
        abort(403)
    user = User.query.get_or_404(id)
    data = request.get_json() or {}
    if 'email' in data and data['email'] != user.email and User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different Email Address')
    user.from_dict(data)
    db.session.commit()
    return jsonify(user.to_dict())

@bp.route('/users/<int:id>',methods=['GET'])
@token_auth.login_required
def get_user(id):
    if token_auth.current_user().id!=id:
        abort(403)
    data = User.query.get_or_404(id).to_dict()
    return jsonify(data)











