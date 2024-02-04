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

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']

        user = User.query.filter_by(username=username).first()

        if not user or not user.verify(pwd):
            return redirect(url_for('login'))
        
        login_user(user)
        redirect(url_for('/'))

    return render_template('login.html')


#Rota para tratar o registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        pwd = request.form['password']

        if user_exists(username, email):
                #Se o usuário já existe no BD4
                return render_template('register.html')
        else:
                
            new_user = User(username=username, email=email, password=pwd)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/recuperar_senha', methods=['GET','POST'])
def recuperar_senha():
    return render_template('recuperar_senha.')

#Fins de teste com BD
@app.route('/<name>/<loc>')
def db_test(name, loc):
    user = User(name=name, location=loc)
    db.session.add(user)
    db.session.commit()

    return '<h1>Added new User</h1>'



if __name__ == '__main__':
    app.run(debug=True)
    
