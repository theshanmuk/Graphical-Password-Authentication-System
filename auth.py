from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db
import random

auth = Blueprint('auth', __name__)

@auth.route('/signup')
def signup():
    #Grahical---Password---Logic to confuse hacker
    N = 6
    images_ = random.sample(range(10, 46), N * N)
    images = []
    for i in range(0, N * N, N):
        images.append(images_[i:i + N])
    return render_template('signup.html',images=images)

@auth.route('/login')
def login():
    #Grahical---Password---Logic to confuse hacker
    N = 6
    images_ = random.sample(range(10, 46), N * N)
    images = []
    for i in range(0, N * N, N):
        images.append(images_[i:i + N])
    return render_template('login.html',images=images)

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.getlist("password")
    password = sorted(password)
    password =''.join(map(str, password))

    # if this returns a user, then the email already exists in database
    user = User.query.filter_by(email=email).first()

    if len(password) < 8:
        flash("password must be minimum 4 selections")
        return redirect(url_for('auth.signup'))

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.getlist('password')
    password = sorted(password)
    password =''.join(map(str, password))
    remember = True if request.form.get('remember') else False
    user = User.query.filter_by(email=email).first()

    if len(password) < 8:
        flash("password must be minimum 4 selections")
        return redirect(url_for('auth.login'))

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))  # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

