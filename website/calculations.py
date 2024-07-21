import pandas as pd
import numpy as np
from geopy.distance import geodesic

def calculate_distance(gps1, gps2):
    return geodesic(gps1, gps2).meters

def process_data(data):
    df = pd.DataFrame(data)
    
    df['Distance'] = df['Gps'].shift(1).combine(df['Gps'], calculate_distance)
    df['Distance'].fillna(0, inplace=True)  # Fill the first NaN value with 0

    # Total distance traveled (in kilometers)
    total_distance_km = df['Distance'].sum() / 1000

    # Total time in hours
    total_time_hours = (df['Timestamp'].iloc[-1] - df['Timestamp'].iloc[0]).total_seconds() / 3600

    # Average speed (km/h)
    average_speed_kmh = total_distance_km / total_time_hours

    # Calorie calculation (assuming an average weight of 70 kg and walking activity)
    weight_kg = 70
    met_walking = 3.5
    calories_burned = weight_kg * met_walking * total_time_hours

    return total_distance_km, average_speed_kmh, calories_burned
