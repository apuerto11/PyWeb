import sqlite3
import click
import os
import hashlib

from flask import Flask, render_template, url_for, redirect, request, current_app, session
from flask.cli import with_appcontext
from flask.helpers import flash

app = Flask(__name__)

AppTitle = "PostIzi"

if not os.path.exists("instance"):
    os.makedirs("instance")


def get_db():
    db = sqlite3.connect(
        os.path.join(app.instance_path, "flaskr.sqlite"),
        detect_types=sqlite3.PARSE_DECLTYPES,
    )
    db.row_factory = sqlite3.Row

    return db


def init_db():
    db = get_db()

    with app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


if not os.path.isfile("instance/flaskr.sqlite"):
    init_db()


def hashMDP(pw):
    m = hashlib.sha256()
    m.update(pw.encode("utf-8"))
    return m.digest()


def dbInsertUser(user, passw, firstname, name):
    db = get_db()

    db.execute(
        "INSERT INTO users (username, password, firstname, name) VALUES (?, ?, ?, ?)",
        (user, hashMDP(passw), name, firstname),
    )
    db.commit()


def dbInsertTask(name, desc, ownerId):
    db = get_db()

    db.execute(
        "INSERT INTO tasks (name, description, owner) VALUES (?, ?, ?)",
        (name, desc, ownerId),
    )
    db.commit()


# def login():
#     error=None
#     if request.method == 'POST':
#         if valid_login(request.form['username'],
#         request.form['password']):
#             return
titre = "IziPost"


@app.route("/")
def index(name=None):
    if 'username' in session:
        return render_template('index.html', tittle = titre)

@app.route("/about")
def about():
    return render_template("about.html", title=titre)


@app.route("/loginForm")
def showLoginForm():
    return render_template("loginForm.html", title=titre)


@app.route("/signupForm")
def showSignUpForm():
   return render_template('signupForm.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()
        if user is None:
            error = 'Incorrect username'
        elif not hashMDP(user['password'], password):
            error ='Incorrect password'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        
        flash(error)

    return render_template('index.html', tittle = titre)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def valid_login (username, password):
    error = "identifiant ou mot de passe invalide"
    db = get_db()
    if username == db.execute("Select username from users where username = {{username}} and password = {{password}}"):
        return username
    else:
        return error
   #return render_template('signupForm.html',title=titre)


    db.execute(
        "INSERT INTO users (username, password, firstname, name) VALUES (?, ?, ?, ?)",
        ("apuerto", "password", "Andrea", "Puerto"))
    db.commit()
@app.route("/dbisert")
def insertUser():
    dbInsertUser("user", "password", "firstname", "name")
    dbInsertTask("Test", "TESTETETETETET", 1)
    return redirect(url_for("index"))
