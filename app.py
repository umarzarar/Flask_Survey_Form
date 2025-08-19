from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import re
import os
from dotenv import load_dotenv

# Load environment variables from creds.env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', os.urandom(24))  # fallback if not set

# Database connection
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'authSurveyApp')
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Database connection failed: {err}")
        return None

# Initialize DB tables if not exist
def init_db():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS survey_responses (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                name VARCHAR(100),
                age INT,
                gender VARCHAR(20),
                satisfaction_lab_sessions VARCHAR(100),
                suggestions TEXT,
                preferred_language VARCHAR(50),
                rating_lab_infrastructure VARCHAR(50),
                email VARCHAR(100),
                programming_languages_known VARCHAR(255),
                satisfaction_level_lab_sessions VARCHAR(100),
                favorite_ide VARCHAR(50),
                preferred_lab_time VARCHAR(50),
                additional_feedback TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()

# Validators
def is_valid_email(email):
    regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(regex, email)

def is_strong_password(password):
    if len(password) < 6:
        return False
    if not re.search(r'\d', password):
        return False
    if not re.search(r'[A-Z]', password):
        return False
    return True

# Routes
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password']

        if not username or not email or not password:
            return render_template('signup.html', message="Please fill out all fields.")

        if not is_valid_email(email):
            return render_template('signup.html', message="Invalid email format.")

        if not is_strong_password(password):
            return render_template(
                'signup.html',
                message="Password must be at least 6 characters, include one digit and one uppercase letter."
            )

        hashed_password = generate_password_hash(password)
        conn = get_db_connection()
        if not conn:
            return render_template('signup.html', message="Database connection failed.")

        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                (username, email, hashed_password)
            )
            conn.commit()
        except mysql.connector.Error as err:
            conn.rollback()
            if err.errno == 1062:
                message = "Username or Email already exists."
            else:
                message = f"Database error: {err}"
            cursor.close()
            conn.close()
            return render_template('signup.html', message=message)

        cursor.close()
        conn.close()
        return render_template('signup.html', success="Signup successful! You can now log in.", message=None)

    return render_template('signup.html', message=None)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_email = request.form['username_email'].strip()
        password = request.form['password']

        if not username_email or not password:
            return render_template('login.html', message="Please fill out all fields.")

        conn = get_db_connection()
        if not conn:
            return render_template('login.html', message="Database connection failed.")

        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username=%s OR email=%s", (username_email, username_email))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', message="Invalid username/email or password.")

    return render_template('login.html', message=None)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/survey', methods=['GET', 'POST'])
def survey():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        try:
            form = request.form
            conn = get_db_connection()
            if not conn:
                return render_template('survey.html', message="Database connection failed.")

            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO survey_responses (
                    user_id, name, age, gender,
                    satisfaction_lab_sessions, suggestions,
                    preferred_language, rating_lab_infrastructure,
                    email, programming_languages_known,
                    satisfaction_level_lab_sessions, favorite_ide,
                    preferred_lab_time, additional_feedback
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                session['user_id'], form.get('name'), form.get('age'), form.get('gender'),
                form.get('satisfaction_lab_sessions'), form.get('suggestions'),
                form.get('preferred_language'), form.get('rating_lab_infrastructure'),
                form.get('email'), form.get('programming_languages_known'),
                form.get('satisfaction_level_lab_sessions'), form.get('favorite_ide'),
                form.get('preferred_lab_time'), form.get('additional_feedback')
            ))
            conn.commit()
            cursor.close()
            conn.close()
            return render_template('survey.html', success="Survey submitted successfully.")
        except Exception as e:
            print("Error submitting survey:", e)
            return render_template('survey.html', message="Please fill all required fields.")

    return render_template('survey.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Error handling
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404 - Page Not Found</h1>", 404

if __name__ == '__main__':
    init_db()
    debug_mode = os.getenv("FLASK_DEBUG", "True") == "True"
    app.run(debug=debug_mode)
