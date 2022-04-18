from flask import Flask, render_template, redirect, url_for, request
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired, NumberRange
from dotenv import dotenv_values

config = dotenv_values(".env")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pawhaven.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app)
db = SQLAlchemy(app, session_options={"expire_on_commit": False})


class User(db.Model):
    fname = db.Column(db.String(100), nullable=False)
    lname = db.Column(db.String(100), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    eml = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), primary_key=True, nullable=False)
    mob = db.Column(db.Integer, nullable=False)
    pswd = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


class Animal(db.Model):
    name = db.Column(db.String(100), primary_key=True, nullable=False)
    type = db.Column(db.String(100), nullable=False)
    breed = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    shelter = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Animal {self.name}>'


class Shelter(db.Model):
    name = db.Column(db.String(100), primary_key=True, nullable=False)
    connum = db.Column(db.Integer, nullable=False)
    coneml = db.Column(db.String(100), nullable=False)
    mannme = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Shelter {self.name}>'


class Forum(db.Model):
    title = db.Column(db.String(100), primary_key=True, nullable=False)
    by = db.Column(db.String(100), nullable=False)
    body = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f'<Forum {self.title}>'


db.create_all()

global user


@app.route('/')
def home():
    return render_template('landing.html')


@app.route('/prelogin')
def prelogin():
    return render_template('prelogin.html')


@app.route('/register/<string:type>')
def register(type):
    print(type)
    return render_template('register.html', type=type)


@app.route('/adduser', methods=['GET', "POST"])
def adduser():
    global user
    if request.method == "POST":
        type = request.form.get('type')
        if type != "shelter":
            fname = request.form.get('fname')
            lname = request.form.get('lname')
            age = request.form.get('num')
            eml = request.form.get('email')
            username = request.form.get('username')
            mob = request.form.get('mob')
            pswd = request.form.get('password')
            print(fname, lname, age, eml, username, mob, pswd, type)
            new_user = User(
                fname=fname,
                lname=lname,
                age=age,
                eml=eml,
                username=username,
                mob=mob,
                pswd=pswd,
                type=type
            )
        else:
            fname = request.form.get('fname')
            lname = request.form.get('lname')
            eml = request.form.get('email')
            username = request.form.get('username')
            mob = request.form.get('mob')
            pswd = request.form.get('password')
            print(fname, lname, eml, username, mob, pswd, type)
            new_user = User(
                fname=fname,
                lname=lname,
                eml=eml,
                username=username,
                mob=mob,
                pswd=pswd,
                type=type
            )
        already_exists = db.session.query(User.username).filter_by(username=username).first() is not None
        if already_exists:
            data = ['Uh Oh!!', "This username already exists.", 'Signup Screen', 'signup']
            return render_template("intermd.html", data=data)
        else:
            db.session.add(new_user)
            db.session.commit()
            user = new_user
            data = ['Success!!', "Your account has been created successfully!!", 'Profile', type]
            # if type == "adopter":
            #     data.append('user')
            # elif type == "owner":
            #     data.append('shelter')
            # elif type == "admin":
            #     data.append('admin')
            return render_template("intermd.html", data=data)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/validate', methods=["GET", "POST"])
def validate():
    global user
    if request.method == "GET":
        return redirect(url_for("profile"))
    if request.method == "POST":
        usnm = request.form.get('username')
        pswd = request.form.get('password')
        exists = db.session.query(User.username).filter_by(username=usnm).first() is not None
        print(exists)
        if exists:
            user_to_verify = User.query.get(usnm)
            if (usnm == user_to_verify.username) and (pswd == user_to_verify.pswd):
                user = user_to_verify
                data = ['Success!!', "You have been logged in successfully!!", 'Continue', user.type]
                # if user.type == "user":
                #     data.append('user')
                # elif user.type == "owner":
                #     data.append('shelter')
                # elif user.type == "admin":
                #     data.append('admin')
                return render_template("intermd.html", data=data)
            else:
                data = ['Oops!!', "Your Username and Password Do Not Match", 'Login Screen', 'login']
                return render_template("intermd.html", data=data)
        else:
            data = ['Oops!!', "This Username Does Not Exist", 'Signup Screen', "prelogin"]
            return render_template("intermd.html", data=data)


@app.route('/user')
def user():
    global user
    return render_template("userdash.html", user=user)


@app.route('/adopt')
def adopt():
    global user
    all_animals = db.session.query(Animal).all()
    print(all_animals)
    return render_template('animals.html', user=user, animals=all_animals)


@app.route('/shletersrc')
def sheltersrc():
    global user
    all_shelters = db.session.query(User).filter_by(type="shelter").all()
    return render_template('shelters.html', user=user, shelters=all_shelters)


@app.route('/shelter')
def shelter():
    global user
    return render_template("shelterdash.html", user=user)


@app.route('/admin')
def admin():
    global user
    return render_template("admindash.html", user=user)


@app.route('/forum')
def forum():
    global user
    all_posts = db.session.query(Forum).all()
    return render_template('forum.html', all_posts=all_posts, user=user)


@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
    global user
    if request.method == "GET":
        return render_template('addpost.html', user=user)
    elif request.method == "POST":
        title = request.form.get('title')
        body = request.form.get('content')
        by = user.username
        new_post = Forum(
            title=title,
            body=body,
            by=by
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('forum'))


@app.route('/lbp')
def lbp():
    global user
    return render_template("lbp.html", user=user)


@app.route('/about')
def about():
    global user
    return render_template('about.html', user=user)


@app.route('/profile')
def profile():
    global user
    return render_template('userprofile.html', user=user)


@app.route('/editprofile', methods=['GET', 'POST'])
def editprofile():
    global user
    if request.method == "POST":
        user_update = User.query.get(user.username)
        user_update.fname = request.form.get('fname')
        user_update.lname = request.form.get('lname')
        user_update.age = request.form.get('age')
        user_update.mob = request.form.get('cnum')
        user_update.eml = request.form.get('email')
        user_update.pswd = request.form.get('pswd')
        db.session.commit()
        data = ['Success!!', "Your profile has been updated successfully.", 'Dashboard', user.type]
        return render_template('intermd.html', data=data)


@app.route('/animalmng')
def animalmng():
    global user
    animals = db.session.query(Animal).filter_by(shelter=user.username).all()
    print(animals)
    return render_template('manageanimal.html', user=user, animals=animals)


@app.route('/animaladd', methods=['GET', 'POST'])
def animaladd():
    global user
    if request.method == 'GET':
        return render_template('animaladd.html', user=user)
    elif request.method == 'POST':
        name = request.form.get('name')
        type = request.form.get('type')
        breed = request.form.get('breed')
        age = request.form.get('age')
        shelter = request.form.get('shelter')
        con = request.form.get('contact')
        new_animal = Animal(
            name=name,
            type=type,
            breed=breed,
            age=age,
            shelter=shelter,
            contact=con
        )
        db.session.add(new_animal)
        db.session.commit()
        data = ['Success!!', "The animal data has been added successfully!!", 'Animal Management', 'animalmng']
        return render_template('intermd.html', data=data)


@app.route('/delanim/<string:name>')
def delanim(name):
    global user
    del_animal = db.session.query(Animal).filter_by(name=name).first()
    db.session.delete(del_animal)
    db.session.commit()
    data = ['Success!!', "The animal data has been deleted successfully!!", 'Animal Management', 'animalmng']
    return render_template('intermd.html', data=data)


@app.route('/logout')
def logout():
    data = ['GoodBye', "Thank you for visiting our site", 'Logout', 'home']
    return render_template("intermd.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)
