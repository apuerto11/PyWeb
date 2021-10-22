import sqlite3
import click
import os

from flask import Flask, render_template, url_for, redirect, request, current_app, g
from flask.cli import with_appcontext

app = Flask(__name__)

AppTitle= "PostIzi"

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

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('initialized the database')

init_db()

# def login():
#     error=None
#     if request.method == 'POST':
#         if valid_login(request.form['username'],
#         request.form['password']):
#             return
titre = "IziPost"

@app.route("/")
def index(name=None):
    return render_template('index.html',title=titre)

@app.route("/about")
def about():
    return render_template('about.html',title=titre)

@app.route("/loginForm")
def showLoginForm():
   return render_template('loginForm.html',title=titre)

@app.route("/signupForm")
def showSignUpForm():
   return render_template('signupForm.html',title=titre)

@app.route("/dbinit")
def initDB():
    init_db_command()
