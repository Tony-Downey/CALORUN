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

from flask import Flask, request, render_template
from flask_login import current_user
import pandas as pd
import json
from datetime import datetime
from math import radians, sin, cos, sqrt, atan2
from io import StringIO

@auth.route('/calculate', methods=['GET', 'POST'])
def calculate():
    if request.method == 'POST':        
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file:
            def haversine_distance(lat1, lon1, lat2, lon2):
                R = 6371  # Earth's radius in kilometers

                lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
                
                dlat = lat2 - lat1
                dlon = lon2 - lon1
                
                a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
                c = 2 * atan2(sqrt(a), sqrt(1-a))
                
                distance = R * c
                return distance

            from io import StringIO

            def parse_csv(file):
                data = []
                prev_lat = prev_lon = prev_time = None
                total_distance = 0
                first_timestamp = None
                last_timestamp = None
                
                # Read the file content and decode it
                file_content = file.stream.read().decode('utf-8')
                
                # Create a file-like object from the string
                csv_file = StringIO(file_content)
                
                next(csv_file)  # Skip the header row
                for line in csv_file:
                    time_str, value_str = line.strip().split(',', 1)
                    
                    timestamp = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
                    value = json.loads(value_str)
                    
                    lat, lon = value['lat'], value['lon']
                    
                    if first_timestamp is None:
                        first_timestamp = timestamp
                    last_timestamp = timestamp
                    
                    if prev_lat is not None:
                        distance = haversine_distance(prev_lat, prev_lon, lat, lon)
                        time_diff = (timestamp - prev_time).total_seconds() / 3600  # Convert to hours
                        
                        if time_diff > 0:
                            speed = distance / time_diff  # km/h
                        else:
                            speed = 0
                        
                        total_distance += distance
                    else:
                        distance = 0
                        speed = 0
                    
                    data.append({
                        'timestamp': timestamp,
                        'latitude': lat,
                        'longitude': lon,
                        'distance': distance,
                        'speed': speed
                    })
                    
                    prev_lat, prev_lon, prev_time = lat, lon, timestamp
                
                total_time = (last_timestamp - first_timestamp).total_seconds() / 3600  # in hours
                avg_speed = total_distance / total_time if total_time > 0 else 0
                
                return total_distance, total_time, avg_speed

            # Usage
            total_distance, total_time, average_speed = parse_csv(file)

            # Calorie calculation (simplified model)
            calories_per_km = 60
            total_calories = total_distance * calories_per_km
            
            def format_time(hours):
                total_seconds = int(hours * 3600)  # Convert hours to seconds
                hours, remainder = divmod(total_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            formatted_time = format_time(total_time)
            
            # Return the results
            results = {
                'total_distance': round(total_distance,2),
                'average_speed': round(average_speed,2),
                'total_calories': round(total_calories),
                'total_time': formatted_time
            }
            return render_template('home.html', user=current_user, results=results)
    
    return render_template('calculate.html', user=current_user)