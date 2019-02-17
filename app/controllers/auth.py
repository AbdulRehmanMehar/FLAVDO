from flask import Blueprint
from ..models import db, User

router = Blueprint('rotuer', __name__)

@router.route('/')
def auth():
    user = User()
    user.username = 'admin'
    user.email = 'admin@localhost'
    # print(user)
    db.session.add(user)
    return 'Hello From Auth'
