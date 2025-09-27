from .base import db
from datetime import datetime
import json

class Symptom(db.Model):
    __tablename__ = 'symptoms'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100))
    severity_level = db.Column(db.String(50))
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'severity_level': self.severity_level
        }

class DiagnosisHistory(db.Model):
    __tablename__ = 'diagnosis_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    symptoms = db.Column(db.Text, nullable=False)
    diagnosed_disease = db.Column(db.String(200), nullable=False)
    confidence_score = db.Column(db.Float, nullable=False)
    recommended_medicines = db.Column(db.Text)
    precautions = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_symptoms(self, symptoms_list):
        self.symptoms = json.dumps(symptoms_list)
    
    def get_symptoms(self):
        return json.loads(self.symptoms) if self.symptoms else []
    
    def set_medicines(self, medicines_list):
        self.recommended_medicines = json.dumps(medicines_list)
    
    def get_medicines(self):
        return json.loads(self.recommended_medicines) if self.recommended_medicines else []