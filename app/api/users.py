from app.api import bp
from flask import jsonify,request,url_for
from app.models import User,Conversation,Anonyuser
from app.api.errors import bad_request
from app import db
import uuid


@bp.route('/users',methods=['POST'])
def create_user():
    data =request.get_json() or {}
    if 'username' not in data or 'email' not in data or 'firstname' not in data or 'lastname' not in data:
        return bad_request('Must include FIRST NAME,LAST_NAME,USERNAME,EMAIL')
    if User.query.filter_by(username=data['username']).first():
        return bad_request(f'Use a different username as {data["username"]} is taken!')
    if User.query.filter_by(username=data['email']).first():
        return bad_request(f'Use a different email as {data["email"]} has been used!')
    user = User()
    user.from_dict(data,new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code=201
    response.headers['location'] = url_for('api.get_user',id=user.id)
    return response


@bp.route('/anony_users',methods=['POST'])
def create_anony_user():
    while True:
        user_id = str(uuid.uuid4())
        if  not Anonyuser.query.filter_by(username=user_id).first():
            user = Anonyuser()
            data = request.get_json() or {}
            user.from_dict(user_id,data) 
            db.session.add(user)
            db.session.commit()
            response = jsonify(user.to_dict())
            response.status_code=201
            response.headers['location'] = url_for('api.add_anony_chat',user_id=user.username)
            return response


@bp.route('/anony_users/<string:user_id>/chat',methods=['POST'])
def add_anony_chat(user_id):
    conversation = Conversation()
    conversation.from_dict(user_id,new_chat=True,anony=True)
    db.session.add(conversation)
    db.session.commit()
    response = jsonify(conversation.to_dict())
    response.status_code=201
    response.headers['location'] = url_for('api.get_anony_chat',user_id=user_id)
    return response

@bp.route('/anony_users/<string:user_id>/chat',methods=['GET'])
def get_anony_chat(user_id):
    data = Conversation.query.filter_by(anony_user_id=user_id).first_or_404().to_dict()
    return jsonify(data)

@bp.route('/anony_users/<string:user_id>/chat',methods=['PUT'])
def update_anony_chat(user_id):
    conversation = Conversation.query.filter_by(anony_user_id=user_id).first_or_404()
    data = request.get_json() or {}
    if  'user_message' not in  data:
        return bad_request('Specify and Ensure message is in data')
    conversation.from_dict(user_id,data=data,anony=True)
    db.session.commit()
    return jsonify(conversation.to_dict())





