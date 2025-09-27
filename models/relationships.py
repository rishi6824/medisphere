from models.base import db
from models.user import User
from models.diagnosis import DiagnosisHistory
from models.chat import ChatHistory

def setup_relationships():
    """Setup relationships after all models are defined to avoid circular imports"""
    
    # User relationships
    if not hasattr(User, 'diagnoses'):
        User.diagnoses = db.relationship('DiagnosisHistory', backref='user', lazy=True, cascade='all, delete-orphan')
    
    if not hasattr(User, 'chats'):
        User.chats = db.relationship('ChatHistory', backref='user', lazy=True, cascade='all, delete-orphan')