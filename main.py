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
@app.route('/progress')
def progress():
    return render_template('progress.html')

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
