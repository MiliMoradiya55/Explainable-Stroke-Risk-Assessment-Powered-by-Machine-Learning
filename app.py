from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os
import database as db
import utils

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

db.init_users_db()
db.init_stroke_db()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        mobile = request.form['mobile']
        hashed = generate_password_hash(password)
        if db.create_user(username, hashed, mobile):
            flash('Account created! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username already exists or invalid data.', 'danger')
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.get_user_by_username(username)
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Logged in successfully.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    user_id = session['user_id']
    predictions = db.get_user_predictions(user_id)
    return render_template('dashboard.html', predictions=predictions[:5])

@app.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    if request.method == 'POST':
        try:
            # Print form data for debugging (optional)
            print("Form data received:", dict(request.form))

            data = {
                'gender': request.form['gender'],
                'age': float(request.form['age']),
                'hypertension': int(request.form.get('hypertension', 0)),
                'heart_disease': int(request.form.get('heart_disease', 0)),
                'ever_married': request.form['ever_married'],
                'work_type': request.form['work_type'],
                'residence_type': request.form['residence_type'],
                'avg_glucose_level': float(request.form['avg_glucose_level']),
                'bmi': float(request.form['bmi']) if request.form['bmi'] else None,
                'smoking_status': request.form['smoking_status']
            }
            pred, proba = utils.predict_stroke(data)
            db.save_prediction(session['user_id'], data, pred, proba)
            flash('Prediction saved!', 'success')
            return redirect(url_for('history'))
        except Exception as e:
            print("❌ Prediction error:", e)  # Print to console
            flash(f'Error making prediction: {str(e)}', 'danger')
    return render_template('prediction_form.html')

@app.route('/history')
@login_required
def history():
    predictions = db.get_user_predictions(session['user_id'])
    return render_template('history.html', predictions=predictions)

@app.route('/report/<int:pred_id>')
@login_required
def report(pred_id):
    pred = db.get_prediction(pred_id, session['user_id'])
    if not pred:
        flash('Prediction not found.', 'danger')
        return redirect(url_for('history'))
    return render_template('report.html', pred=pred)

@app.route('/explain')
def explain():
    return render_template('explain.html')

@app.route('/chart')
@login_required
def chart():
    predictions = db.get_user_predictions(session['user_id'])
    return render_template('chart.html', predictions=predictions)

if __name__ == '__main__':
    if not os.path.exists('stroke_model.pkl'):
        print("⚠️  Model files missing. Please run train_model.py first.")
    else:
        app.run(debug=True)