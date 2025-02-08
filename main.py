from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import random
import csv
import io, base64, matplotlib.pyplot as plt
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

@app.route('/weather', methods=['GET'])
def weather():
    # Get the latitude and longitude from the query parameters
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    if lat and lon:
        api_key = "your_openweathermap_api_key_here"  # Replace with your actual API key
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        
        try:
            # Make the request to the OpenWeatherMap API
            response = requests.get(url)
            weather_data = response.json()

            if response.status_code == 200:  # If the request is successful
                # Extract relevant data
                weather = {
                    "city": weather_data.get("name"),
                    "temperature": weather_data["main"]["temp"],
                    "description": weather_data["weather"][0]["description"],
                    "icon": weather_data["weather"][0]["icon"]
                }
                return render_template('weather.html', weather=weather)
            else:
                return jsonify({"error": "Unable to fetch weath er data"}), 400
        except requests.exceptions.RequestException as e:
            return jsonify({"error": f"An error occurred: {e}"}), 500
    else:
        return jsonify({"error": 'Location (lat/lon) not provided'}), 400


@app.route('/export_csv')
@login_required
def export_csv():
    filename = "workouts.csv"
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["workout_name", "steps", "duration", "calories", "heart_rate", "workout_date"])
        writer.writeheader()
        writer.writerows(workouts)
    return redirect(url_for('dashboard'))

steps_data = [2000, 4000, 6000, 8000, 10000]
dates = ['2025-02-01', '2025-02-02', '2025-02-03', '2025-02-04', '2025-02-05']

# Route for the graph page
@app.route('/graph')
def graph():
    # Create a graph using the dummy data
    fig, ax = plt.subplots()
    ax.plot(dates, steps_data, marker='o', color='b', label='Steps')

    # Add labels and title
    ax.set_xlabel('Date')
    ax.set_ylabel('Steps')
    ax.set_title('Steps Over Time')

    # Save the plot to a BytesIO object and encode it in base64 to embed in HTML
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    # Pass the plot to the HTML page
    return render_template('graph.html', plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True)
