from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again', category="error")
        else:
            flash('Username does not exist.', category='error')
        
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if len(username) < 2:
            flash('Invalid username (must be greater than 1 characters)', category='error') #Message flashing funtion of Flask
        elif password != confirm_password:
            flash('Password don\'t match', category='error')
        elif len(password) < 7:
            flash('Invalid password(must be greater then 6 characters)', category='error')
        else:
            new_user = User(username = username, password = generate_password_hash(password, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit() 
            
            flash('Account successfully created', category='success')
            
            return redirect(url_for('views.home'))
            
    return render_template("sign_up.html",user=current_user)

from flask import Blueprint, render_template, request
import pandas as pd
import numpy as np
from geopy.distance import geodesic

# Define the new route for calculations
@auth.route('/calculate', methods=['GET', 'POST'])
def calculate():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            # Load the uploaded CSV file
            df = pd.read_csv(file)

            # Calculate distance between consecutive GPS coordinates
            def haversine_distance(lat1, lon1, lat2, lon2):
                return geodesic((lat1, lon1), (lat2, lon2)).meters

            distances = []
            for i in range(1, len(df)):
                lat1, lon1 = map(float, df['Gps'][i-1].split(','))
                lat2, lon2 = map(float, df['Gps'][i].split(','))
                distance = haversine_distance(lat1, lon1, lat2, lon2)
                distances.append(distance)

            # Add distance column
            distances.insert(0, 0)  # No distance for the first point
            df['Distance'] = distances

            # Calculate total distance
            total_distance = df['Distance'].sum() / 1000  # in kilometers

            # Calculate average speed
            total_time_hours = (pd.to_datetime(df['Timestamp'].iloc[-1]) - pd.to_datetime(df['Timestamp'].iloc[0])).total_seconds() / 3600
            average_speed = total_distance / total_time_hours  # in km/h

            # Calorie calculation (simplified model)
            calories_per_km = 60
            total_calories = total_distance * calories_per_km

            # Return the results
            results = {
                'total_distance': total_distance,
                'average_speed': average_speed,
                'total_calories': total_calories
            }
            return render_template('home.html', results=results)
    
    return render_template('calculate.html', user=current_user)