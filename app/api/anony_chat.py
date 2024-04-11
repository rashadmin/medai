from app.api import bp
from flask import jsonify,request,url_for
from app.models import Conversation
from app.api.errors import bad_request
from app import db



@bp.route('/anony_users/<string:user_id>/chat',methods=['POST'])
def add_anony_chat(user_id):
    conversation = Conversation()
    conversation.from_dict(user_id,new_chat=True,anony=True)
    db.session.add(conversation)
    db.session.commit()
    response = jsonify(conversation.to_anony_dict())
    response.status_code=201
    response.headers['location'] = url_for('api.get_anony_chat',user_id=user_id)
    return response


@bp.route('/anony_users/<string:user_id>/chat',methods=['GET'])
def get_anony_chat(user_id):
    data = Conversation.query.filter_by(anony_user_id=user_id).first_or_404().to_anony_dict()
    return jsonify(data)

@bp.route('/anony_users/<string:user_id>/chat',methods=['PUT'])
def update_anony_chat(user_id):
    conversation = Conversation.query.filter_by(anony_user_id=user_id).first_or_404()
    data = request.get_json() or {}
    if  'user_message' not in  data:
        return bad_request('Specify and Ensure message is in data')
    conversation.from_dict(user_id,data=data,anony=True)
    db.session.commit()
    return jsonify(conversation.to_anony_dict())
