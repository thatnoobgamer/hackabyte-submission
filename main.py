import sqlite3
from flask import Flask, render_template, request, redirect, url_for, Response
import plotly.express as px
import plotly.io as pio
import pandas as pd  # Importing pandas for data manipulation
from datetime import datetime

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('workouts.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS workouts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    workout_name TEXT,
                    steps INTEGER,
                    duration INTEGER,
                    calories INTEGER,
                    heart_rate INTEGER,
                    workout_date TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    conn = sqlite3.connect('workouts.db')
    c = conn.cursor()
    workouts = request.form.getlist('workout-name')
    steps = request.form.getlist('steps')
    duration = request.form.getlist('duration')
    calories = request.form.getlist('calories')
    heart_rate = request.form.getlist('heart-rate')
    workout_date = request.form.getlist('workout-date')

    for i in range(len(workouts)):
        c.execute("INSERT INTO workouts (workout_name, steps, duration, calories, heart_rate, workout_date) VALUES (?, ?, ?, ?, ?, ?)",
                  (workouts[i], steps[i], duration[i], calories[i], heart_rate[i], workout_date[i]))
    
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/graph')
def graph():
    conn = sqlite3.connect('workouts.db')
    c = conn.cursor()
    c.execute("SELECT * FROM workouts")
    data = c.fetchall()
    conn.close()
    
    # Convert data to a pandas DataFrame for easy manipulation
    df = pd.DataFrame(data, columns=['id', 'workout_name', 'steps', 'duration', 'calories', 'heart_rate', 'workout_date'])
    
    # Create a line plot to visualize steps over time
    fig = px.line(df, x='workout_date', y='steps', title='Steps Progress Over Time')
    graph_html = pio.to_html(fig, full_html=False)
    
    return render_template('graph.html', graph_html=graph_html)

@app.route('/export_csv')
def export_csv():
    conn = sqlite3.connect('workouts.db')
    c = conn.cursor()
    c.execute('SELECT * FROM workouts')
    data = c.fetchall()
    conn.close()

    # Prepare CSV data from database
    output = Response(
        '\n'.join([','.join(map(str, row)) for row in data]),
        mimetype='text/csv'
    )
    output.headers["Content-Disposition"] = "attachment; filename=workouts.csv"
    return output

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
