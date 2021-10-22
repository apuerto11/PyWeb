from flask import Flask, render_template, url_for, redirect, request, session

app = Flask(__name__)


@app.route("/")
def index(name=None):
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/loginForm")
def showLoginForm():
   return render_template('loginForm.html')

@app.route("/signupForm")
def showSignUpForm():
   return render_template('signupForm.html')

@app.route("/login/seConnecter", methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        valid_login('username', 'password')
        session['username'] = request.form['username']
        return

#def valid_login (user, password):
 #   error = "identifiant ou mot de passe invalide"
 #   if (user == Select name from user where name = 'user' and password = "password"):
  #      name = select name from user where mail = user or name = name
   #     return name
   # else:
    #    return error