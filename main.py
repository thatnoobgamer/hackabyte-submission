from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import random
import csv
import os
import requests

# Initialize Flask App
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
login_manager = LoginManager()
login_manager.init_app(app)

# In-memory storage for demo purposes
users = {'test': {'password': 'password123'}}  # Replace with real database
workouts = []  # List to store workout data

# Fitness tips for motivation
fitness_tips = [
    "Stay hydrated!",
    "Consistency is key!",
    "Push yourself to the limit!"
]

# User Model
class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    return User(user_id, 'test')

# Routes
@app.route('/')
def index():
    tip = random.choice(fitness_tips)  # Display a random fitness tip
    return render_template('index.html', tip=tip)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            user = User(username, username)
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.username, workouts=workouts)

@app.route('/submit', methods=['POST'])
@login_required
def submit_workout():
    workout_data = {
        'workout_name': request.form['workout-name'],
        'steps': request.form['steps'],
        'duration': request.form['duration'],
        'calories': request.form['calories'],
        'heart_rate': request.form['heart-rate'],
        'workout_date': request.form['workout-date'],
    }
    workouts.append(workout_data)
    return redirect(url_for('dashboard'))

@app.route('/leaderboard')
def leaderboard():
    # Sort workouts by steps (this can be expanded for leaderboard logic)
    sorted_workouts = sorted(workouts, key=lambda x: int(x['steps']), reverse=True)
    return render_template('leaderboard.html', workouts=sorted_workouts)

import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/weather')
def weather():
    # Get latitude and longitude from the query string
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    if lat and lon:
        # Use OpenWeatherMap API to get the weather data
        api_key = "68c62c52de388d389eb3f205e9e7b45c"
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
        response = requests.get(url)
        weather_data = response.json()

        return jsonify(weather_data)
    else:
        return jsonify({'error': 'Location not provided'}), 400

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/export_csv')
@login_required
def export_csv():
    filename = "workouts.csv"
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["workout_name", "steps", "duration", "calories", "heart_rate", "workout_date"])
        writer.writeheader()
        writer.writerows(workouts)
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
