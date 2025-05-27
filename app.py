from flask import Flask, render_template, request, redirect, url_for, flash
import csv
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'super-secret-poggy-woggy'  # Change this to a random secret key

# CSV file to store user data
CSV_FILE = 'user_data.csv'

def init_csv():
    """Initialize CSV file with headers if it doesn't exist"""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Email', 'Feedback', 'Timestamp'])

def save_to_csv(name, email, feedback):
    """Save user data to CSV file"""
    with open(CSV_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        writer.writerow([name, email, feedback, timestamp])

def read_from_csv():
    """Read all user data from CSV file"""
    data = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'r') as file:
            reader = csv.DictReader(file)
            data = list(reader)
    return data

@app.route('/')
def home():
    """Homepage with welcome message"""
    return render_template('home.html')

@app.route('/form')
def form():
    """Form page to input user data"""
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    """Handle form submission"""
    name = request.form['name']
    email = request.form['email']
    feedback = request.form['feedback']
    
    # Basic validation
    if not name or not email or not feedback:
        flash('All fields are required!', 'error')
        return redirect(url_for('form'))
    
    # Save data to CSV
    save_to_csv(name, email, feedback)
    
    # Pass data to result page
    return render_template('result.html', name=name, email=email, feedback=feedback)

@app.route('/data')
def view_data():
    """Optional: View all submitted data"""
    data = read_from_csv()
    return render_template('data.html', data=data)

if __name__ == '__main__':
    init_csv()
    app.run(debug=True)