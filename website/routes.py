# website/routes.py

from flask import Blueprint, render_template, flash, redirect, url_for
from website import app
from website.forms import LoginForm, RegistrationForm, PostForm
from .models import User

main = Blueprint('main', __name__)

@main.route('/')
def home():
    user = User.query.first()  # Example: Get the first user from the database
    return render_template('home.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.email.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Registration requested for user {}'.format(form.email.data))
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)

@app.route('/post', methods=['GET', 'POST'])
def post():
    form = PostForm()
    if form.validate_on_submit():
        flash('Post created with title {}'.format(form.title.data))
        return redirect(url_for('index'))
    return render_template('post.html', title='Create Post', form=form)
