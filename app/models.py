from app import db,login
from dateutil.relativedelta import relativedelta
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash 
from flask_login import UserMixin
import enum
from app.chat.chat import chat,Information
from app.videos.video_functions import return_url
from json.decoder import JSONDecodeError
from flask import url_for
import json
import google.generativeai as genai

model = genai.GenerativeModel('gemini-pro')

class Gender(enum.Enum):
    male = 'Male'
    female = 'Female'
    not_to_say = 'I Prefer not to say'
class BloodGroup(enum.Enum):
    a_positive = 'A+'
    b_positive = 'B+'
    ab_positive = 'AB+'
    o_positive = 'O+'
    a_negative = 'A-'
    b_negative = 'B-'
    ab_negative = 'AB-'
    o_negative = 'O-'
class Genotype(enum.Enum):
    AA = 'AA'
    AS = 'AS'
    SS = 'SS'
    SC = 'SC'
    AC = 'AC'

class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query,page,per_page,endpoint,**kwargs):
        resources = query.paginate(page=page,per_page=per_page,error_out=False)
        data = {
            'chats':[item.to_dict() for item in resources.items],
            '_meta':{
                'page':page,
                'per_page':per_page,
                'total_pages':resources.pages,
                'total_items':resources.total
            },
            '_links':{
                'self':url_for(endpoint,page=page,per_page=per_page,**kwargs),
                'prev':url_for(endpoint,page=page-1,per_page=per_page,**kwargs) if resources.has_prev else None,
                'next':url_for(endpoint,page=page+1,per_page=per_page,**kwargs) if resources.has_next else None,
            }
        }
        return data

class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    firstname = db.Column(db.String(25),nullable = False)
    lastname = db.Column(db.String(25),nullable = False)
    username = db.Column(db.String(25),unique=True,nullable = False)
    email =  db.Column(db.String(120),unique=True,nullable = False)
    date_joined = db.Column(db.Date,default=datetime.now)
    date_of_birth = db.Column(db.Date,nullable=False)
    gender = db.Column(db.Enum(Gender))
    password_hash = db.Column(db.String(200),nullable = False)
    bloodgroup = db.Column(db.Enum(BloodGroup))
    genotype = db.Column(db.Enum(Genotype))
    medical_history = db.Column(db.Text)
    conversations = db.Relationship('Conversation',backref = 'user')
    
    
    def __repr__(self):
        return f'<User : {self.username}, Email : {self.email}>'
    

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)


    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def conversations_history_by_last_created(self):
        history = Conversation.query.filter_by(user_id=self.id)
        return history.order_by(Conversation.created_at.desc())
    def conversations_history_by_last_updated(self):
        history = Conversation.query.filter_by(user_id=self.id)
        return history.order_by(Conversation.modified_at.desc())    
    def to_dict(self):
        data = {
            'id' : self.id,
            'first_name':self.firstname,
            'last_name': self.lastname,
            'username':self.username,
            'email':self.email,
            'gender':self.gender.value if self.gender else None,
            'Age':relativedelta(datetime.now(),self.date_of_birth).years,
            'bloodgroup':self.bloodgroup.value if self.bloodgroup else None,
            'genotype':self.genotype.value if self.genotype else None,
            'medical_history':self.medical_history,
            '_links':{
                'self': url_for('api.get_user',id=self.id),
                'conversations':url_for('api.get_chats',id=self.id)}
        }
        return data
    def from_dict(self,data,new_user=False):
        for field in ['first_name','last_name','username','email','gender','date_of_birth','bloodgroup','genotype','medical_history']:
            if field in data:
                setattr(self,field,data[field])
            if field == 'date_of_birth':
                date = eval(data['date_of_birth'])
                self.date_of_birth = datetime(date[0],date[1],date[2])
        if new_user and 'password' in data:
            self.set_password(data['password'])

class Anonyuser(UserMixin,db.Model):
    username = db.Column(db.String(50),primary_key=True)
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.Enum(Gender))
    date_created = db.Column(db.Date,default=datetime.now)
    bloodgroup = db.Column(db.Enum(BloodGroup))
    genotype = db.Column(db.Enum(Genotype))
    medical_history = db.Column(db.Text)
    conversations = db.Relationship('Conversation',backref = 'anonyuser',uselist=False)
    
    
    def __repr__(self):
        return f'<User : {self.username}'

    def to_dict(self):
        data = {
            'username':self.username,
            'Gender':self.gender.value if self.gender else None,
            'Age':relativedelta(datetime.now(),self.date_of_birth).years,
            'bloodgroup':self.bloodgroup.value if self.bloodgroup else None,
            'genotype':self.genotype.value if self.genotype else None,
            'medical_history':self.medical_history,
            '_links':{
                #'self': url_for('api.get_user',id=self.id),
                'conversations':url_for('api.get_anony_chat',user_id=self.username)}
        }
        return data
    def from_dict(self,user_id,data=None):
        self.username = user_id
        for field in ['bloodgroup','genotype','medical_history','gender','date_of_birth']:
            if field in data and field != 'date_of_birth':
                setattr(self,field,data[field])
            if field == 'date_of_birth':
                date = eval(data['date_of_birth'])
                self.date_of_birth = datetime(date[0],date[1],date[2])


            

class Conversation(PaginatedAPIMixin,db.Model):
    __searchable__ = ['title','message']
    id = db.Column(db.Integer,primary_key=True)
    conversation_no =  db.Column(db.Integer,nullable = True)
    created_at = db.Column(db.Date,default=datetime.now)
    modified_at = db.Column(db.Date,default=datetime.now)
    title = db.Column(db.String(120),nullable = False)
    message = db.Column(db.Text,nullable = False)
    is_dict_done = db.Column(db.Boolean)
    youtube_link = db.Column(db.Text,nullable=True)
    info_hospital = db.Column(db.Text,nullable=True) 
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    anony_user_id = db.Column(db.String(50),db.ForeignKey('anonyuser.username'))
    hospitals = None
    def __repr__(self):
        return f'<User : {self.user_id} Conversation_Number : {self.conversation_no}, Title : {self.title}, Created : {self.created_at}>'

    def to_dict(self):
        data = {
            'id' : self.id,
            'conversation_no':self.conversation_no,
            'created_at': self.created_at.isoformat() + 'Z',
            'modified_at':self.modified_at.isoformat() + 'Z',
            'title':self.title,
            'message':json.loads(self.message)[2:],
            'length': self.check_length(),
            '_links':{'youtube_link':self.youtube_link,
                      'hospital_link':url_for('api.hospital_info_for_anony',user_id=self.anony_user_id)}

        }
        return data
   

    def from_dict(self,user_id,conversation_no=None,new_chat=False,data=None,anony=False):
        if new_chat:
            message = chat()
            self.created_at = datetime.now()
            self.message = message.return_all_message()
            self.modified_at = datetime.now()
            self.is_dict_done = False
            if anony:
                self.anony_user_id = user_id
                self.title = f'mychat'
            else:
                self.user_id = user_id
                self.conversation_no = conversation_no
                self.title = f"{user_id}'s chat_{conversation_no}"
        if not new_chat:
            #CChatBot message 
            message = chat(history=json.loads(self.message))
            message.add_user_message(prompt=data['user_message'])
            if not self.is_dict_done:
                information = Information()
                information.add_user_message(data['user_message'])
                dict_response = information.return_information()
            
            # Information message
            if dict_response:
                self.info_hospital = repr(dict_response)
                try:
                    if 'FirstAid_searchwords' in dict_response.keys():
                        search_keywords = dict_response['FirstAid_searchwords']
                    elif dict_response['Situation'] == 'non medical related condition':
                        search_keywords=None
                    elif 'FirstAid_searchwords' not in dict_response.keys():
                        search_keywords=None
                except JSONDecodeError:
                    search_keywords = None
                print('info',search_keywords)
                if search_keywords:
                    returned_link = [return_url(keyword) for keyword in search_keywords]
                    print('info2',returned_link)
                    if all(returned_link) is False:
                        self.youtube_link = None
                    elif any(returned_link) is False:
                        returned_link_temp = {repr(i) for i in returned_link if i is not False}
                        returned_link = [eval(i) for i in returned_link_temp]
                        self.youtube_link = repr(returned_link)
                    else:
                        returned_link_temp = {repr(i) for i in returned_link}
                        returned_link = [eval(i) for i in returned_link_temp]
                        self.youtube_link = repr(returned_link)
                    self.is_dict_done = True
            self.message = message.return_all_message()
            self.modified_at = datetime.now()
    def check_length(self):
        return model.count_tokens(json.loads(self.message)).total_tokens
    def to_hospital_dict(self):
        print(self.info_hospital)
        info = eval(self.info_hospital)
        if info['Situation'] == 'non medical related condition':
            return None
        if 'FirstAid_searchwords' in info:
            info.pop('FirstAid_searchwords')
        return info


@login.user_loader
def load_user(id):
    return db.session.get(User,int(id))


