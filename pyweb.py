import sqlite3
import click
import os
from flask.cli import with_appcontext
from flask.helpers import flash
from flask import (
    Flask,
    render_template,
    url_for,
    redirect,
    request,
    current_app,
    session,
)

app = Flask(__name__)
titre = "IziPost"

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



###################### Route ##########################
### Index HTML ###
@app.route("/")
def index():
    # if "username" in session:
    return render_template("index.html", title=titre)
        
### about HTML ###
@app.route("/about")
def about():
    return render_template('about.html',title=titre)
### Connection page HTML ###
@app.route("/loginForm")
def showLoginForm():
   return render_template('loginForm.html',title=titre)
### Sign-Up Page HTML ###
@app.route("/signupForm")
def showSignUpForm():
    return render_template("signupForm.html", title=titre)


### Application en elle meme (visible dans le header pour raison de developpement)###
@app.route("/iziPostApp")
def showApp():
    return render_template('iziPostApp.html', title=titre)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        if user is None:
            error = "Incorrect username"
        elif not hashMDP(user["password"], password):
            error = "Incorrect password"

        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))

        flash(error)

    return render_template("index.html", title=titre) # Pourquoi afficher quand meme l'index ici ?

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
###################### End Route ##########################

if not os.path.exists('instance'):
    os.makedirs('instance')

def get_db():
    db = sqlite3.connect(
        os.path.join(app.instance_path, 'flaskr.sqlite'),
        detect_types=sqlite3.PARSE_DECLTYPES
    )
    db.row_factory = sqlite3.Row

    return db

def init_db():
    db = get_db()

    with app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

if not os.path.isfile('instance/flaskr.sqlite'):
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


@app.route("/dbisert")
def insertDB():
    db = get_db()

    db.execute(
        "INSERT INTO users (username, password, firstname, name) VALUES (?, ?, ?, ?)",
        ("apuerto", "password", "Andrea", "Puerto"),
    )
    db.commit()


# return render_template('signupForm.html',title=titre)


@app.route("/dbisert")
def insertUser():
    dbInsertUser("user", "password", "firstname", "name")
    dbInsertTask("Test", "TESTETETETETET", 1)
    return redirect(url_for("index"))
