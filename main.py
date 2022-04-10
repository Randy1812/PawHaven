from flask import Flask, render_template, redirect, url_for, request
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired, NumberRange

app = Flask(__name__)
Bootstrap(app)


@app.route('/')
def home():
    return render_template('landing.html')


@app.route('/prelogin')
def prelogin():
    return render_template('prelogin.html')


@app.route('/register/<string:type>')
def register(type):
    print(type)
    return render_template('register.html')


@app.route('/login')
def login():
    return render_template('login.html')


if __name__ == "__main__":
    app.run(debug=True)
