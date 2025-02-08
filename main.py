from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
import datetime
import matplotlib.pyplot as plt
import io
import base64
import requests

app = Flask(__name__)

# JSON File to Store Data
DATA_FILE = 'workouts.json'

# Load existing data or create an empty list
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return []

# Save data to JSON file
def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Home Route (Workout Input Form)
@app.route('/', methods=['GET', 'POST'])
def home():
    workouts = load_data()

    if request.method == 'POST':
        workout = {
            "date": str(datetime.date.today()),
            "workout_name": request.form.get('workout_name'),
            "steps": request.form.get('steps'),
            "heart_rate": request.form.get('heart_rate'),
            "calories_burned": request.form.get('calories_burned'),
            "distance_walked": request.form.get('distance_walked')
        }
        workouts.append(workout)
        save_data(workouts)
        return redirect(url_for('home'))

    return render_template('index.html', workouts=workouts)

# API to Get Data (for Debugging or Future Use)
@app.route('/data')
def get_data():
    return jsonify(load_data())

# Graphs Route
@app.route('/graphs')
def graphs():
    workouts = load_data()

    if not workouts:
        return "No data available to plot.", 404

    dates = [w['date'] for w in workouts]
    steps = [int(w['steps']) for w in workouts]
    heart_rates = [int(w['heart_rate']) for w in workouts if w['heart_rate']]
    calories = [float(w['calories_burned']) for w in workouts if w['calories_burned']]
    distances = [float(w['distance_walked']) for w in workouts if w['distance_walked']]

    # Create Subplots for Multiple Graphs
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))

    # Steps Graph
    axes[0, 0].plot(dates, steps, marker='o', color='b', label='Steps')
    axes[0, 0].set_title("Steps Over Time")
    axes[0, 0].set_xlabel("Date")
    axes[0, 0].set_ylabel("Steps")

    # Heart Rate Graph
    if heart_rates:
        axes[0, 1].plot(dates[:len(heart_rates)], heart_rates, marker='s', color='r', label='Heart Rate')
        axes[0, 1].set_title("Heart Rate Over Time")
        axes[0, 1].set_xlabel("Date")
        axes[0, 1].set_ylabel("Heart Rate (bpm)")

    # Calories Burned Graph
    if calories:
        axes[1, 0].plot(dates[:len(calories)], calories, marker='^', color='g', label='Calories Burned')
        axes[1, 0].set_title("Calories Burned Over Time")
        axes[1, 0].set_xlabel("Date")
        axes[1, 0].set_ylabel("Calories")

    # Distance Walked Graph
    if distances:
        axes[1, 1].plot(dates[:len(distances)], distances, marker='x', color='purple', label='Distance Walked')
        axes[1, 1].set_title("Distance Walked Over Time")
        axes[1, 1].set_xlabel("Date")
        axes[1, 1].set_ylabel("Distance (km)")

    plt.tight_layout()

    # Save plot as base64
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    return render_template('graphs.html', plot_url=plot_url)

# Progress Report Route
@app.route('/progress')
def progress():
    workouts = load_data()

    if not workouts:
        return "No progress data available.", 404

    weekly_steps = sum([int(w['steps']) for w in workouts if datetime.datetime.strptime(w['date'], '%Y-%m-%d') >= datetime.datetime.today() - datetime.timedelta(days=7)])
    monthly_steps = sum([int(w['steps']) for w in workouts if datetime.datetime.strptime(w['date'], '%Y-%m-%d') >= datetime.datetime.today() - datetime.timedelta(days=30)])

    return render_template('progress.html', weekly_steps=weekly_steps, monthly_steps=monthly_steps)

# Weather Route (Location & Weather)
@app.route('/weather')
def weather():
    # Example API for weather (replace with actual API and key)
    api_key = "68c62c52de388d389eb3f205e9e7b45c"
    location = "London"
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"

    response = requests.get(weather_url).json()

    temperature = response['main']['temp'] - 273.15  # Convert from Kelvin to Celsius
    weather_desc = response['weather'][0]['description']

    return render_template('weather.html', temperature=temperature, weather_desc=weather_desc)

@app.route('/get_weather')
def get_weather():
    # Get latitude and longitude from the query parameters
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    API_KEY = "68c62c52de388d389eb3f205e9e7b45c"
    # Construct the URL for OpenWeatherMap API
    url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric'

    # Make the API request to OpenWeatherMap
    response = requests.get(url)
    weather_data = response.json()

    # Return the weather data as JSON
    return jsonify(weather_data)

if __name__ == '__main__':
    app.run(debug=True)
