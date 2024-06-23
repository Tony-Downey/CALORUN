from flask import Blueprint, render_template, request, flash
from flask_login import current_user


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html", message='This is the Login Page', user=current_user, boolean = True)


@auth.route('/logout')
def logout():
    return "<p>logout<p>"


@auth.route('/sign-up', methods=['GET', 'POST'])
def Sign_up():  
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('Invalid email(must be greater than 3 characters)', category='error') #Message flashing funtion of Flask
        elif len(firstName) < 2:
            flash('Invalid Name(must be greater than 1 characters)', category='error')
        elif password1 != password2:
            flash('Password don\'t match', category='error')
        elif len(password1) < 7:
            flash('Invalid password(must be greater then 6 characters)', category='error')
        else:
            flash('Account successfully created', category='success')


    return render_template("sign_up.html", user=current_user)

