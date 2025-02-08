from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import plotly.express as px
import plotly.io as pio
import json

app = Flask(__name__)

# Set up SQLite database
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS workouts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    workout_name TEXT,
                    steps INTEGER,
                    duration INTEGER,
                    calories INTEGER,
                    heart_rate INTEGER)''')
    conn.commit()
    conn.close()

init_db()

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Save data route
@app.route('/submit', methods=['POST'])
def submit():
    workout_name = request.form['workout-name']
    steps = request.form['steps']
    duration = request.form['duration']
    calories = request.form['calories']
    heart_rate = request.form['heart-rate']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''INSERT INTO workouts (workout_name, steps, duration, calories, heart_rate) 
                 VALUES (?, ?, ?, ?, ?)''', 
              (workout_name, steps, duration, calories, heart_rate))
    conn.commit()
    conn.close()

    return redirect(url_for('home'))

# Graph route
@app.route('/graph')
def graph():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM workouts')
    data = c.fetchall()
    conn.close()

    # Prepare the data for graphing
    workouts = [row[1] for row in data]  # workout_name
    steps = [row[2] for row in data]
    duration = [row[3] for row in data]
    calories = [row[4] for row in data]

    # Create a DataFrame using Plotly
    fig = px.bar(x=workouts, y=steps, title="Steps per Workout")
    graph_html = pio.to_html(fig, full_html=False)

    return render_template('graph.html', graph_html=graph_html)

if __name__ == '__main__':
    app.run(debug=True)
