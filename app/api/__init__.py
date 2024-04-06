from flask import Blueprint
bp = Blueprint('api',__name__)
from app.api import users,chat,errors,hospital,anony_chat,anony_user