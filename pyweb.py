"""IziPost main module"""

import sqlite3
import os
import hashlib
from flask.helpers import flash
from flask import (
    Flask,
    render_template,
    url_for,
    redirect,
    request,
    # current_app,
    session,
)
app = Flask(__name__)
app.secret_key = "t\xdd\xe7\xe2\xda\xa2\xc0^\xd7%\x19t`\xfeg\x1e\xbe"
MyList= ""


TITRE = "IziPost"

if not os.path.exists("instance"):
    os.makedirs("instance")


def get_database():
    """Get database"""
    database = sqlite3.connect(
        os.path.join(app.instance_path, "flaskr.sqlite"),
        detect_types=sqlite3.PARSE_DECLTYPES,
    )
    database.row_factory = sqlite3.Row

    return database


def init_database():
    """Initialization of database"""
    database = get_database()

    with app.open_resource("schema.sql") as file:
        database.executescript(file.read().decode("utf8"))


if not os.path.isfile("instance/flaskr.sqlite"):
    init_database()


def hash_mdp(password):
    """Encrypt password
    Keyword arguments:
    pw -- Password to encrypt as string
    """

    not_hashed = hashlib.sha256()
    not_hashed.update(password.encode("utf-8"))
    return not_hashed.digest()


# owner_id n'est pas un parametre il faut que la méthode recupere directement l'id de l'utilisateur et la mette en parametre
@app.route("/createTask",  methods=('GET','POST'))
# def createTask(name, desc, status, owner_id):
def createTask():
    if request.method == 'POST':
         
        TaskStatus = request.form.get('selectSection')
        print(TaskStatus)
        name=request.form.get('TaskTitle')
        desc=request.form.get('TaskContent')

        database = get_database()
    
        database.execute(
          "INSERT INTO tasks (name, description, status, owner) VALUES (?, ?, ?, ?)",
         # (name, desc, status, owner_id),
            (name, desc, TaskStatus, session["id"]),
        )
        database.commit()

    return redirect(url_for("show_app"))


def database_update_task(task_id, name, description, status):
    """Update a task in the database"""
    database = get_database()
    database.execute(
        "UPDATE tasks SET name = ?, description = ?, status = ? WHERE id = ?",
        (name, description, status, task_id),
        database.commit(),
    )



def database_delete_tasks(task_id):
    """delete a task with a specific ID"""
    if request.method == "POST":
        database = get_database()
        database.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        database.commit()


if not os.path.exists("instance"):
    os.makedirs("instance")


if not os.path.isfile("instance/flaskr.sqlite"):
    init_database()


### Index HTML ###
@app.route("/")
def index():
    """Index routing"""
    # if "username" in session:
    return render_template("index.html", title=TITRE)


### about HTML ###
@app.route("/about")
def about():
    """About routing"""
    return render_template("about.html", title=TITRE)

# @app.route('MainApp')
# def database_fetch_tasks():
#     """get all tasks from a user"""
#     database = get_database()
#     tasks = database.execute(
#         "SELECT * FROM tasks t INNER JOIN users u on t.owner = u.id WHERE u.username = ?",
#         (session["username"]),
#     ).fetchall()

#     return tasks

@app.route("/iziPostApp")
def show_app():
    """App routing"""

    database = get_database()
    tasks = database.execute(
        "SELECT * FROM tasks t INNER JOIN users u on t.owner = u.id WHERE u.username = ? ORDER BY id desc",
        (session["username"]),
    ).fetchall()
    print(tasks)
    return render_template("IziPostApp.html", title=TITRE, lengthTasks = len(tasks), tasks = tasks)


@app.route("/createNewTaskPage")
def create_new_task_page():
    return render_template("createNewTaskPage.html",title=TITRE)


@app.route("/register", methods=("GET", "POST"))
def register():
    """Register routing"""
    print("Register method called")
    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]

        database = get_database()
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."

        if error is None:
            try:
                database.execute(
                    "INSERT INTO users (username, password, firstname, name) VALUES (?, ?, ?, ?)",
                    (username, hash_mdp(password), firstname, lastname),
                )
                database.commit()
            except database.IntegrityError:
                error = "Pseudo already used."
                flash(error)
            else:
                return redirect(url_for("login"))

        return redirect(url_for("register"))
    return render_template("signupForm.html", title=TITRE)


@app.route("/login", methods=("GET", "POST"))
def login():
    """Login routing"""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        database = get_database()
        error = None
        user = database.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        if user is None:
            error = "Incorrect username"
        elif not hash_mdp(password) == user["password"]:
            error = "Incorrect password"

        if error is None:
            session.clear()
            session["username"] = user["username"]
            session["id"] = user["id"]
            return redirect(url_for("show_app"))

        flash(error)
        return redirect(url_for("login"))

    return render_template("loginForm.html", title=TITRE)


@app.route("/logout")
def logout():
    """Logout routing"""
    session.clear()
    return redirect(url_for("index"))


###################### End Route ##########################