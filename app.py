from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import Config
from models.base import db
from models.user import User
from utils.database import init_db
from services.auth_service import AuthService
from services.diagnosis_engine import DiagnosisEngine
from services.medicine_recommender import MedicineRecommender
from services.hospital_locator import HospitalLocator
from services.chatbot_engine import ChatbotEngine
import json
from datetime import datetime

# Initialize services
auth_service = AuthService()
diagnosis_engine = DiagnosisEngine()
medicine_recommender = MedicineRecommender()
hospital_locator = HospitalLocator()
chatbot_engine = ChatbotEngine()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    init_db(app)
    
    # Setup login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message = 'Please log in to access this page.'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    return app

app = create_app()

# Routes
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        # Pass the form data directly without converting date
        form_data = request.form.to_dict()
        
        user, errors = auth_service.register_user(form_data)
        
        if errors:
            for field, message in errors.items():
                flash(message, 'error')
            return render_template('auth/register.html')
        
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('auth/register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        user, error = auth_service.authenticate_user(
            request.form['email'], 
            request.form['password']
        )
        
        if error:
            flash(error, 'error')
            return render_template('auth/login.html')
        
        login_user(user)
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        flash(f'Welcome back, {user.first_name}!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('auth/login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.first_name = request.form['first_name']
        current_user.last_name = request.form['last_name']
        current_user.phone_number = request.form.get('phone_number', '')
        current_user.address = request.form.get('address', '')
        current_user.city = request.form.get('city', '')
        current_user.state = request.form.get('state', '')
        current_user.pincode = request.form.get('pincode', '')
        current_user.blood_group = request.form.get('blood_group', '')
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('profile.html', user=current_user)

@app.route('/diagnosis', methods=['GET', 'POST'])
@login_required
def diagnosis():
    from models.diagnosis import Symptom, DiagnosisHistory
    
    if request.method == 'POST':
        symptoms = request.form.getlist('symptoms')
        additional_symptoms = request.form.get('additional_symptoms', '')
        
        if additional_symptoms:
            symptoms.extend([s.strip() for s in additional_symptoms.split(',') if s.strip()])
        
        disease, confidence = diagnosis_engine.diagnose(symptoms)
        medicines = medicine_recommender.recommend_medicines(disease)
        precautions = diagnosis_engine.get_precautions(disease)
        
        # Save diagnosis history
        diagnosis_record = DiagnosisHistory(
            user_id=current_user.id,
            diagnosed_disease=disease,
            confidence_score=confidence
        )
        diagnosis_record.set_symptoms(symptoms)
        diagnosis_record.set_medicines(medicines)
        diagnosis_record.precautions = '\n'.join(precautions)
        
        db.session.add(diagnosis_record)
        db.session.commit()
        
        return render_template('diagnosis_result.html', 
                             disease=disease,
                             confidence=confidence,
                             medicines=medicines,
                             precautions=precautions,
                             symptoms=symptoms)
    
    # Get available symptoms for selection
    symptoms = Symptom.query.all()
    return render_template('diagnosis.html', symptoms=symptoms)

@app.route('/medicines')
@login_required
def medicines():
    search_query = request.args.get('search', '')
    medicines_list = []
    
    if search_query:
        # Simple search implementation
        all_medicines = medicine_recommender.medicines_data
        for disease, meds in all_medicines.items():
            for med in meds:
                if search_query.lower() in med['name'].lower():
                    med_info = med.copy()
                    med_info['disease'] = disease
                    med_info['details'] = medicine_recommender.get_medicine_details(med['name'])
                    medicines_list.append(med_info)
    
    return render_template('medicines.html', 
                         medicines=medicines_list, 
                         search_query=search_query)

@app.route('/hospitals')
@login_required
def hospitals():
    user_lat = request.args.get('lat', type=float)
    user_lon = request.args.get('lon', type=float)
    city = request.args.get('city', '')
    state = request.args.get('state', '')
    
    hospitals_list = []
    
    if user_lat and user_lon:
        # Find nearby hospitals
        hospitals_list = hospital_locator.find_nearby_hospitals(user_lat, user_lon)
    elif city or state:
        # Search by location
        hospitals_list = hospital_locator.search_hospitals(city=city, state=state)
    else:
        # Show all hospitals
        hospitals_list = hospital_locator.hospitals_df.to_dict('records')
    
    return render_template('hospitals.html', 
                         hospitals=hospitals_list,
                         city=city,
                         state=state)

@app.route('/chat', methods=['POST'])
@login_required
def chat():
    from models.chat import ChatHistory
    
    message = request.json.get('message', '')
    
    if not message:
        return jsonify({'error': 'Empty message'}), 400
    
    response = chatbot_engine.generate_response(message)
    is_medical = chatbot_engine.is_medical_question(message)
    
    # Save chat history
    chat_record = ChatHistory(
        user_id=current_user.id,
        message=message,
        response=response,
        is_medical_question=is_medical
    )
    db.session.add(chat_record)
    db.session.commit()
    
    return jsonify({
        'response': response,
        'is_medical': is_medical
    })

@app.route('/chat_history')
@login_required
def chat_history():
    from models.chat import ChatHistory
    chats = ChatHistory.query.filter_by(user_id=current_user.id)\
                           .order_by(ChatHistory.created_at.desc())\
                           .limit(50).all()
    
    return jsonify([chat.to_dict() for chat in chats])

if __name__ == '__main__':
    app.run(debug=True)