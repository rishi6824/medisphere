from models.base import db, setup_models
from models.diagnosis import Symptom

def init_db(app):
    """Initialize the database with the app"""
    db.init_app(app)
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Setup relationships after tables are created
        setup_models()
        
        # Add sample data
        add_sample_data()

def add_sample_data():
    """Add sample medical data to the database"""
    # Check if symptoms already exist
    if Symptom.query.first() is not None:
        print("Sample data already exists")
        return
    
    # Add sample symptoms
    symptoms = [
        {'name': 'Cough', 'category': 'Respiratory', 'severity_level': 'Mild'},
        {'name': 'Fever', 'category': 'General', 'severity_level': 'Moderate'},
        {'name': 'Headache', 'category': 'Neurological', 'severity_level': 'Mild'},
        {'name': 'Sore throat', 'category': 'Respiratory', 'severity_level': 'Mild'},
        {'name': 'Runny nose', 'category': 'Respiratory', 'severity_level': 'Mild'},
        {'name': 'Shortness of breath', 'category': 'Respiratory', 'severity_level': 'Severe'},
        {'name': 'Chest pain', 'category': 'Cardiac', 'severity_level': 'Severe'},
        {'name': 'Nausea', 'category': 'Gastrointestinal', 'severity_level': 'Moderate'},
        {'name': 'Vomiting', 'category': 'Gastrointestinal', 'severity_level': 'Moderate'},
        {'name': 'Diarrhea', 'category': 'Gastrointestinal', 'severity_level': 'Moderate'},
        {'name': 'Fatigue', 'category': 'General', 'severity_level': 'Mild'},
        {'name': 'Muscle pain', 'category': 'Musculoskeletal', 'severity_level': 'Mild'},
        {'name': 'Joint pain', 'category': 'Musculoskeletal', 'severity_level': 'Moderate'},
        {'name': 'Rash', 'category': 'Dermatological', 'severity_level': 'Mild'},
        {'name': 'Dizziness', 'category': 'Neurological', 'severity_level': 'Moderate'},
    ]
    
    for symptom_data in symptoms:
        symptom = Symptom(**symptom_data)
        db.session.add(symptom)
    
    db.session.commit()
    print("Sample symptoms added to database")