from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import User, Note
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)

from flask import Blueprint, render_template, request
import pandas as pd
import numpy as np
from geopy.distance import geodesic

views = Blueprint('views', __name__)

# Define the new route for calculations
@views.route('/calculate', methods=['GET', 'POST'])
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
            return render_template('results.html', results=results)
    
    return render_template('calculate.html')
