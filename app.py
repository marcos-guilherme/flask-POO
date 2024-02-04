from flask import Flask, render_template
from database import db
from main import app


#Configuração do BD
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db.init_app(app)

#Criação das tabelas a partir dos models
with app.app_context():
    db.create_all()



