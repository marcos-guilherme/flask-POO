from flask import Flask
from database import db
from flask import render_template, request, redirect, url_for
from models import User
from flask_login import login_user, logout_user
from extensions import login_manager
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

@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        user = User.query.filter_by(email=email).first()

        if not user or not user.verify(senha):
            return redirect(url_for('login'))
        
        login_user(user)
        return redirect(url_for('home'))

    return render_template('login.html')


#Rota para tratar o registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']

        if user_exists(username, username):
                #Se o usuário já existe no BD4
                return render_template('register.html')
        else:
                
            new_user = User(username=username,password=pwd)
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


#Fins de teste com BD
@app.route('/<name>/<loc>')
def db_test(name, loc):
    user = User(name=name, location=loc)
    db.session.add(user)
    db.session.commit()

    return '<h1>Added new User</h1>'



if __name__ == '__main__':
    app.run(debug=True)
    
