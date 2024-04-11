from app.api import bp
from flask import jsonify,request,url_for
from app.models import User,Conversation,Anonyuser
from app.api.errors import bad_request
from app import db
import uuid
from app.api.tokens import token_auth


@bp.route('/anony_users',methods=['POST'])
def create_anony_user():
    while True:
        user_id = str(uuid.uuid4())
        if  not Anonyuser.query.filter_by(username=user_id).first():
            if token_auth.get_auth():
                referrer = User.query.filter_by(token=token_auth.get_auth().token).first().id
            else:
                referrer=None
            user = Anonyuser()
            data = request.get_json() or {}
            user.from_dict(user_id,referrer,data) 
            db.session.add(user)
            db.session.commit()
            response = jsonify(user.to_dict())
            response.status_code=201
            response.headers['location'] = url_for('api.add_anony_chat',user_id=user.username)
            return response
        
    {
        "firstname":"Bayo",
        "lastname":"Ade",
        "username":"bays",
        "email":"abdul.a.rasheed2022@gmail.com",
        "date_of_birth":"(1992, 6, 1)",
        "bloodgroup":"a_positive",
        "genotype":"SS",
        "medical_history":"I have asthma",
        "gender":"male",
        "password":"ayom0908"
    }
{
    "user_message":"my wife was stabbed"
}