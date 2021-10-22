from logging import error
from flask import Flask, render_template, url_for, redirect, request

app = Flask(__name__)

AppTitle= "PostIzi"

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