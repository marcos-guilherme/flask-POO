from datetime import datetime
from database import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin



#Teste de criação de Models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, autoincrement=True ,primary_key=True)
    username = db.Column(db.String(86), nullable=False)
    email = db.Column(db.String(86), nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def verify(self, pwd):
        return check_password_hash(self.password, pwd)
    

