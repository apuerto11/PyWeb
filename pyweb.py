import sqlite3
import click
import os
import hashlib
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
    """Get DB"""
    db = sqlite3.connect(
        os.path.join(app.instance_path, "flaskr.sqlite"),
        detect_types=sqlite3.PARSE_DECLTYPES,
    )
    db.row_factory = sqlite3.Row

    return db

def init_db():
    """Initialization of DB"""
    db = get_db()

    with app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


if not os.path.isfile("instance/flaskr.sqlite"):
    init_db()


def hashMDP(pw):
    """Encrypt password
       
    Keyword arguments:
    pw -- Password to encrypt as string
    """
    m = hashlib.sha256()
    m.update(pw.encode("utf-8"))
    return m.digest()


def dbInsertUser(user, passw, firstname, name):
    """Creation of user profile
       
    Keyword arguments:
    user -- username as string
    passw -- Unencrypted password as string
    firstname -- firstname of the user as string
    name -- lastname of the user as string
    """
    db = get_db()

    db.execute(
        
        "INSERT INTO users (username, password, firstname, name) VALUES (?, ?, ?, ?)",
        (user, hashMDP(passw), name, firstname),
    )
    db.commit()


def dbInsertTask(name, desc, ownerId):
    """Insert user task in DB
    
    Keyword arguments:
    name -- lastname of the user as string
    desc -- description of the task
    ownerID -- The ID of the owner"""
    db = get_db()

    db.execute(
        "INSERT INTO tasks (name, description, owner) VALUES (?, ?, ?)",
        (name, desc, ownerId),
    )
    db.commit()

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


### Index HTML ###
@app.route("/")
def index():
    # if "username" in session:
    return render_template("index.html", title=titre)
        
### about HTML ###
@app.route("/about")
def about():
    return render_template("about.html", title=titre)

### Application en elle meme (visible dans le header pour raison de developpement)###
@app.route("/iziPostApp")
def showApp():
    return render_template("iziPostApp.html", title=titre)


@app.route("/login", methods=("GET", "POST"))
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
        return redirect(url_for("login"))
    else:

        return render_template("loginForm.html", title=titre)

@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO users (username, password, firstname, name) VALUES (?, ?, ?, ?)",
                    (username, hashMDP(password), firstname, lastname),
                )
                db.commit()
            except db.IntegrityError:
                error = f'User{username} is already registered.'
            else:
                return redirect(url_for("login"))
            
        flash(error)
        return redirect(url_for("register"))

    return render_template("signupForm.html", title=titre)    

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/dbisert")
def insertUser():
    dbInsertUser("user", "password", "firstname", "name")
    dbInsertTask("Test", "TESTETETETETET", 1)
    return redirect(url_for("index"))
###################### End Route ##########################