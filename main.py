from curses import flash
from flask import Flask
from flask import render_template, request, redirect, url_for
from database import db
from models import User

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


#Rota para tratar o registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    
    return render_template('register.html')


#Fins de teste com BD
@app.route('/<name>/<loc>')
def db_test(name, loc):
    user = User(name=name, location=loc)
    db.session.add(user)
    db.session.commit()

    return '<h1>Added new User</h1>'








if __name__ == '__main__':
    app.run(debug=True)
    
    
