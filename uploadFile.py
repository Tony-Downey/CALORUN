from flask import Flask, request, render_template, jsonify
import pandas as pd
from calculations import process_data

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    
    if file:
        data = pd.read_csv(file)  # Assuming the uploaded file is a CSV
        data['Gps'] = data['Gps'].apply(eval)  # Convert GPS string to list
        total_distance_km, average_speed_kmh, calories_burned = process_data(data)
        return jsonify({
            "total_distance_km": total_distance_km,
            "average_speed_kmh": average_speed_kmh,
            "calories_burned": calories_burned
        })

if __name__ == '__main__':
    app.run(debug=True)
