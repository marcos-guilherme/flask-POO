from database import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from extensions import login_manager


@login_manager.user_loader
def get_user(user_id):
    return User.query.filter_by(id=user_id)

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    genero = db.Column(db.String(64), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    nome = db.Column(db.String(128), nullable=False)
    cpf = db.Column(db.String(128), nullable=False, unique=True)
    cond = db.Column(db.String(16), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, genero, idade, nome, cpf, cond, user_id):
        self.genero = genero
        self.idade = idade
        self.nome = nome
        self.cpf = cpf
        self.cond = cond
        self.user_id = user_id




#Teste de criação de Models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, autoincrement=True ,primary_key=True)
    username = db.Column(db.String(86), nullable=False, unique=True)
    email = db.Column(db.String(86), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    empresa = db.Column(db.String(128), nullable=False)
    estado = db.Column(db.String(16), nullable=False)
    telefone = db.Column(db.String(128), nullable=False)
    clientes = db.relationship('Cliente', backref='user', lazy=True)



    def __init__(self, username, email, password, empresa, estado, telefone):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.empresa = empresa
        self.estado = estado
        self.telefone = telefone


    def verify(self, pwd):
        return check_password_hash(self.password, pwd) 
    

