from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import all models here after db is created
from models.user import User
from models.diagnosis import Symptom, DiagnosisHistory
from models.chat import ChatHistory

def setup_models():
    """Setup model relationships after all models are imported"""
    # User relationships
    User.diagnoses = db.relationship('DiagnosisHistory', backref='user', lazy=True, cascade='all, delete-orphan')
    User.chats = db.relationship('ChatHistory', backref='user', lazy=True, cascade='all, delete-orphan')