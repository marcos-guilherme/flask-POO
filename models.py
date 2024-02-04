from database import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from extensions import login_manager


@login_manager.user_loader
def get_user(user_id):
    return User.query.filter_by(id=user_id)






#Teste de criação de Models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, autoincrement=True ,primary_key=True)
    username = db.Column(db.String(86), nullable=False, unique=True)
    email = db.Column(db.String(86), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def verify(self, pwd):
        return check_password_hash(self.password, pwd) 
    

