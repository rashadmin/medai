from app.api import bp
from flask import jsonify,request,url_for,abort
from app.models import Conversation,User
from app.api.errors import bad_request
from app import db
from app.api.tokens import token_auth


@bp.route('/users/<int:id>/chats/<int:chat_id>',methods=['GET'])
@token_auth.login_required
def get_chat(id,chat_id):
    if token_auth.current_user().id!=id:
        abort(403)
    data = Conversation.query.filter_by(user_id=id,conversation_no=chat_id).first_or_404().to_dict()
    return jsonify(data)

@bp.route('/users/<int:id>/chats',methods=['GET'])
@token_auth.login_required
def get_chats(id):
    if token_auth.current_user().id!=id:
        abort(403)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Conversation.to_collection_dict(Conversation.query.filter_by(user_id=id),id=id,page=page,per_page=per_page,endpoint='api.get_chats')
    return data

@bp.route('/users/<int:id>/chats/<int:chat_id>',methods=['PUT'])
@token_auth.login_required
def update_chat(id,chat_id):
    if token_auth.current_user().id!=id:
        abort(403)
    conversation = Conversation.query.filter_by(user_id=id,conversation_no=chat_id).first_or_404()
    data = request.get_json() or {}
    if  'user_message' not in  data:
        return bad_request('Specify the Conversation number and Ensure message is in data')
    conversation.from_dict(id,data=data)
    db.session.commit()
    return jsonify(conversation.to_dict())


@bp.route('/users/<int:id>/chats',methods=['POST'])
@token_auth.login_required
def add_chat(id):
    if token_auth.current_user().id!=id:
        abort(403)
    conversation = Conversation()
    conversation_no = Conversation.query.filter_by(user_id=id).count() + 1
    user = User.query.get_or_404(id)
    username = user.to_dict()['username']
    conversation.from_dict(id,username=username,conversation_no=conversation_no,new_chat=True)
    db.session.add(conversation)
    db.session.commit()
    response = jsonify(conversation.to_dict())
    response.status_code=201
    response.headers['location'] = url_for('api.get_chat',id=id,chat_id=conversation_no)
    return response