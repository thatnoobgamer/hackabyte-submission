from flask import Flask, render_template, request, redirect, url_for, jsonify
import datetime
import matplotlib.pyplot as plt
import io
import base64
import requests

app = Flask(__name__)

# Home Route (Workout Input Form)
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

# API to Get Data (for Debugging or Future Use)
@app.route('/data')
def get_data():
    return jsonify([])  # No data from backend now; everything is handled by frontend

# Graphs Route
@app.route('/graphs')
def graphs():
    return render_template('graphs.html')

# Progress Report Route
@app.route('/history')
def progress():
    return render_template('history.html')

# Weather Route (Location & Weather)
# Weather Route (Location & Weather)
@app.route('/weather')
def weather():
    api_key = "68c62c52de388d389eb3f205e9e7b45c"
    location = "London"
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"

    try:
        response = requests.get(weather_url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        data = response.json()

        temperature = data['main']['temp'] - 273.15  # Convert from Kelvin to Celsius
        weather_desc = data['weather'][0]['description']

        return render_template('weather.html', temperature=temperature, weather_desc=weather_desc)
    except requests.exceptions.RequestException as e:
        # Handle errors (network issues, invalid API key, etc.)
        return f"An error occurred: {e}"

@app.route('/get_weather')
def get_weather():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    API_KEY = "68c62c52de388d389eb3f205e9e7b45c"

    if not lat or not lon:
        return jsonify({"error": "Location parameters (lat, lon) are required."}), 400

    url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric'

    try:
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()

        # Check if the data returned is valid
        if 'weather' not in weather_data:
            return jsonify({"error": "Weather data not found."}), 404

        return jsonify(weather_data)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error fetching weather data: {e}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
