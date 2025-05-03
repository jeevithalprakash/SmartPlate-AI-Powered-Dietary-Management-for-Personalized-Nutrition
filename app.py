from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import uuid
import base64
import requests
import json
import re
import math
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure file upload settings
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

db = SQLAlchemy(app)

# Database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    number = db.Column(db.String(15), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    health_data = db.relationship('HealthData', backref='user', lazy=True)

class HealthData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    age = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    food_image = db.Column(db.String(255), nullable=True)
    food_name = db.Column(db.String(100), nullable=True)
    nutrition_info = db.Column(db.Text, nullable=True)
    assessment = db.Column(db.Text, nullable=True)
    diet_plan = db.Column(db.Text, nullable=True)
    recommendation = db.Column(db.Text, nullable=True)

# Helper functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def calculate_bmi(weight, height):
    # Height in meters (convert from cm)
    height_m = height / 100
    bmi = weight / (height_m * height_m)
    return round(bmi, 2)

def analyze_food_with_gemini(image_path, user_data):
    """
    Analyze food image using Google's Gemini API
    """
    try:
        # Google Gemini API settings
        API_KEY = "AIzaSyAOr1fscByIEIHVs6Gav-90_wV9hVE8IE4"  # Your Gemini API key
        API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        
        # Read the image file and convert to base64
        with open(image_path, "rb") as image_file:
            image_bytes = image_file.read()
            image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        
        # Extract user data for context
        age = user_data['age']
        weight = user_data['weight']
        height = user_data['height']
        gender = user_data['gender']
        bmi = calculate_bmi(weight, height)
        
        # Create prompt for the API with user context
        prompt = f"""
        Analyze this food image in detail:
        1. Identify what food item(s) are in the image
        2. Provide detailed nutritional information (calories, protein, carbs, fat, vitamins, etc.)
        3. Assess if this food is suitable for a person with these health metrics:
           - Age: {age} years
           - Gender: {gender}
           - Height: {height} cm
           - Weight: {weight} kg
           - BMI: {bmi}
        4. Suggest a personalized diet plan related to this food
        5. Provide a specific recommendation for improving nutrition
        
        Format your response in JSON with these keys:
        {{"food_name": "Name of food", 
         "nutrition": "Detailed HTML formatted nutritional breakdown with <ul> and <li> tags", 
         "good_for_user": "Assessment of suitability for this user", 
         "diet_plan": "Personalized diet plan", 
         "recommendation": "Specific recommendation"}}
        """
        
        # Prepare the request payload
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt},
                        {
                            "inline_data": {
                                "mime_type": "image/jpeg",
                                "data": image_base64
                            }
                        }
                    ]
                }
            ],
            "generation_config": {
                "temperature": 0.4,
                "top_p": 0.95,
                "top_k": 40
            }
        }
        
        # Make the API request
        response = requests.post(
            f"{API_URL}?key={API_KEY}",
            headers={"Content-Type": "application/json"},
            json=payload
        )
        
        # Check if request was successful
        if response.status_code == 200:
            response_data = response.json()
            
            # Extract the text response
            if 'candidates' in response_data and len(response_data['candidates']) > 0:
                text_response = response_data['candidates'][0]['content']['parts'][0]['text']
                
                # Try to parse JSON from the response
                try:
                    # Find JSON in the response (in case there's additional text)
                    import re
                    json_match = re.search(r'({.*})', text_response, re.DOTALL)
                    if json_match:
                        json_str = json_match.group(1)
                        result = json.loads(json_str)
                        
                        # Ensure all required keys are present
                        required_keys = ['food_name', 'nutrition', 'good_for_user', 'diet_plan', 'recommendation']
                        for key in required_keys:
                            if key not in result:
                                result[key] = "Information not available"
                        
                        return result
                except json.JSONDecodeError:
                    # If JSON parsing fails, extract information using regex
                    patterns = {
                        'food_name': r'food_name"?\s*:\s*"([^"]+)"',
                        'nutrition': r'nutrition"?\s*:\s*"(.*?)"(?=,\s*"good_for_user"|,\s*"diet_plan"|,\s*"recommendation"|}})',
                        'good_for_user': r'good_for_user"?\s*:\s*"([^"]+)"',
                        'diet_plan': r'diet_plan"?\s*:\s*"([^"]+)"',
                        'recommendation': r'recommendation"?\s*:\s*"([^"]+)"'
                    }
                    
                    result = {}
                    for key, pattern in patterns.items():
                        match = re.search(pattern, text_response, re.DOTALL)
                        result[key] = match.group(1) if match else "Information not available"
                    
                    # Format nutrition as HTML if it's not already
                    if "<ul>" not in result['nutrition']:
                        nutrition_text = result['nutrition']
                        nutrition_html = "<ul>"
                        for line in nutrition_text.split('\n'):
                            if line.strip():
                                nutrition_html += f"<li>{line.strip()}</li>"
                        nutrition_html += "</ul>"
                        result['nutrition'] = nutrition_html
                    
                    return result
        
        # Fall back to a default response if API call fails or parsing fails
        return {
            'food_name': "Could not analyze food properly",
            'nutrition': "<ul><li>Nutritional information unavailable</li></ul>",
            'good_for_user': "Unable to assess with the current image",
            'diet_plan': "Please consult a nutritionist for personalized advice",
            'recommendation': "Try uploading a clearer image of your food"
        }
    
    except Exception as e:
        print(f"Error in Gemini API call: {e}")
        return {
            'food_name': "Could not identify food",
            'nutrition': "<ul><li>Nutritional information unavailable</li></ul>",
            'good_for_user': "Unable to assess",
            'diet_plan': "Please consult a nutritionist for personalized advice",
            'recommendation': "Try uploading a clearer image of your food"
        }

# Flask routes
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        number = request.form['number']
        name = request.form['name']
        gender = request.form['gender']
        password = generate_password_hash(request.form['password'])

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered.')
            return redirect(url_for('login'))

        new_user = User(email=email, number=number, name=name, gender=gender, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registered successfully.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password_input = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password_input):
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_gender'] = user.gender
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.')
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        flash("Please log in first.")
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Extract form data
        age = int(request.form['age'])
        height = float(request.form['height'])
        weight = float(request.form['weight'])
        
        # Handle file upload
        file = request.files['food_image']
        filename = None
        if file and allowed_file(file.filename):
            # Create unique filename to avoid conflicts
            unique_filename = str(uuid.uuid4()) + secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(filepath)
            
            # Analyze food image using Gemini API
            user_data = {
                'age': age,
                'height': height,
                'weight': weight,
                'gender': session['user_gender']
            }
            
            analysis_result = analyze_food_with_gemini(filepath, user_data)
            
            # Save the data to the database
            health_data = HealthData(
                user_id=session['user_id'],
                age=age,
                height=height,
                weight=weight,
                food_image=unique_filename,
                food_name=analysis_result['food_name'],
                nutrition_info=analysis_result['nutrition'],
                assessment=analysis_result['good_for_user'],
                diet_plan=analysis_result['diet_plan'],
                recommendation=analysis_result['recommendation']
            )
            db.session.add(health_data)
            db.session.commit()
            
            # Calculate BMI
            bmi = calculate_bmi(weight, height)
            
            # Prepare the food image path for display
            food_image_path = url_for('uploaded_file', filename=unique_filename)
            
            return render_template('result.html', 
                                  name=session['user_name'], 
                                  gender=session['user_gender'],
                                  age=age, 
                                  height=height, 
                                  weight=weight,
                                  bmi=bmi,
                                  food_name=analysis_result['food_name'],
                                  nutrition=analysis_result['nutrition'],
                                  good_for_user=analysis_result['good_for_user'],
                                  diet_plan=analysis_result['diet_plan'],
                                  recommendation=analysis_result['recommendation'],
                                  food_image_path=food_image_path)
        else:
            flash("Please upload a valid image file (png, jpg, jpeg).")

    return render_template('dashboard.html', name=session['user_name'], gender=session['user_gender'])

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.")
    return redirect(url_for('login'))

# Function to create DB tables
def create_tables():
    db.create_all()

if __name__ == '__main__':
    with app.app_context():
        create_tables()
    app.run(debug=True)