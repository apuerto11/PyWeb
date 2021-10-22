from flask import Flask, render_template, url_for, redirect, request

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