from flask import flash
from flask import Flask
from database import db
from flask import render_template, request, redirect, url_for
from models import User
from flask_login import login_user, logout_user
from extensions import login_manager
from werkzeug.security import check_password_hash
import secrets

app = Flask(__name__)

app.secret_key = secrets.token_hex(16)

#Configuração do BD
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'


login_manager.init_app(app)
db.init_app(app)

#Criação das tabelas a partir dos models
with app.app_context():
    db.create_all()



def user_exists(username, email):
    user = User.query.filter((User.username == username) | (User.email == email)).first()
    return user is not None

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        user = User.query.filter_by(email=email).first()

        if user is None or not check_password_hash(user.password, senha):
            flash('Email ou senha incorreto, por favor tente novamente.')
            return redirect(url_for('login'))
        
        login_user(user)
        return redirect(url_for('home'))

    return render_template('login.html')


#Rota para tratar o registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        pwd = request.form['password']
        empresa = request.form['empresa']
        estado = request.form['estado']
        telefone = request.form['telephone']

        user = User.query.filter((User.username == username) | (User.email == email)).first()

        if user:

            flash('Email ou Usuário já em uso.')
            return render_template('register.html')

                
        new_user = User(username=username,password=pwd, empresa=empresa,
                            email=email, telefone=telefone, estado=estado)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/recuperar_senha', methods=['GET','POST'])
def recuperar_senha():
    return render_template('recuperar_senha.html')


@app.route('/contato', methods=['GET','POST'])
def contato():
    return render_template('contato.html')

@app.route('/clientes', methods=['GET','POST'])
def clientes():
    return render_template('clientes.html')

if __name__ == '__main__':
    app.run(debug=True)
    
