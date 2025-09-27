import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import os

class DiagnosisEngine:
    def __init__(self):
        self.diseases_data = self.load_diseases_data()
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        self.train_model()
    
    def load_diseases_data(self):
        """Load diseases and their symptoms"""
        diseases = {
            'Common Cold': ['cough', 'fever', 'sore throat', 'runny nose', 'sneezing', 'congestion'],
            'Influenza (Flu)': ['fever', 'cough', 'headache', 'muscle pain', 'fatigue', 'chills'],
            'COVID-19': ['fever', 'cough', 'shortness of breath', 'fatigue', 'loss of taste', 'loss of smell'],
            'Migraine': ['headache', 'nausea', 'sensitivity to light', 'dizziness', 'throbbing pain'],
            'Food Poisoning': ['nausea', 'vomiting', 'diarrhea', 'stomach pain', 'fever', 'headache'],
            'Allergies': ['sneezing', 'runny nose', 'itchy eyes', 'rash', 'congestion'],
            'Asthma': ['shortness of breath', 'wheezing', 'cough', 'chest tightness'],
            'Bronchitis': ['cough', 'shortness of breath', 'fatigue', 'fever', 'chest discomfort'],
            'Pneumonia': ['fever', 'cough', 'chest pain', 'shortness of breath', 'fatigue'],
            'Gastroenteritis': ['nausea', 'vomiting', 'diarrhea', 'stomach cramps', 'fever'],
            'Urinary Tract Infection': ['painful urination', 'frequent urination', 'abdominal pain', 'fever'],
            'Sinusitis': ['headache', 'facial pain', 'runny nose', 'congestion', 'cough'],
            'Hypertension': ['headache', 'dizziness', 'chest pain', 'shortness of breath', 'vision problems'],
            'Diabetes': ['frequent urination', 'excessive thirst', 'fatigue', 'blurred vision', 'weight loss']
        }
        return diseases
    
    def train_model(self):
        """Train the symptom-disease matching model"""
        symptoms_list = []
        diseases_list = []
        
        for disease, symptoms in self.diseases_data.items():
            symptoms_text = ' '.join(symptoms)
            symptoms_list.append(symptoms_text)
            diseases_list.append(disease)
        
        if symptoms_list:
            self.tfidf_matrix = self.vectorizer.fit_transform(symptoms_list)
            self.diseases_list = diseases_list
    
    def diagnose(self, user_symptoms):
        """Diagnose based on user symptoms"""
        if not user_symptoms:
            return "No symptoms provided", 0.0
        
        # Clean and preprocess symptoms
        cleaned_symptoms = [symptom.lower().strip() for symptom in user_symptoms]
        user_symptoms_text = ' '.join(cleaned_symptoms)
        
        try:
            user_vector = self.vectorizer.transform([user_symptoms_text])
            
            # Calculate similarity scores
            similarity_scores = cosine_similarity(user_vector, self.tfidf_matrix)
            max_score_idx = np.argmax(similarity_scores)
            max_score = similarity_scores[0, max_score_idx]
            
            if max_score > 0.1:  # Lower threshold for better matching
                diagnosed_disease = self.diseases_list[max_score_idx]
                return diagnosed_disease, float(max_score)
            
            return "Unknown Condition - Symptoms not recognized", 0.0
            
        except Exception as e:
            return f"Diagnosis error: {str(e)}", 0.0
    
    def get_precautions(self, disease):
        """Get precautions for diagnosed disease"""
        precautions = {
            'Common Cold': [
                'Get plenty of rest and sleep',
                'Drink fluids like water, juice, and clear broth',
                'Use a humidifier to moisten the air',
                'Gargle with warm salt water for sore throat',
                'Avoid smoking and secondhand smoke'
            ],
            'Influenza (Flu)': [
                'Rest and allow your body to recover',
                'Stay hydrated with water and electrolyte drinks',
                'Take antiviral medication if prescribed early',
                'Avoid contact with others to prevent spread',
                'Use fever reducers like acetaminophen as needed'
            ],
            'COVID-19': [
                'Isolate yourself from others for at least 5 days',
                'Monitor your symptoms and oxygen levels',
                'Seek emergency care for trouble breathing',
                'Wear a high-quality mask around others',
                'Get plenty of rest and stay hydrated'
            ],
            'Migraine': [
                'Rest in a quiet, dark room',
                'Apply cold compresses to your head or neck',
                'Stay hydrated and avoid skipping meals',
                'Identify and avoid migraine triggers',
                'Practice relaxation techniques'
            ],
            'Food Poisoning': [
                'Stay hydrated with small sips of water',
                'Avoid solid foods until vomiting stops',
                'Gradually introduce bland foods like crackers',
                'Get plenty of rest',
                'Avoid dairy, caffeine, alcohol, and fatty foods'
            ]
        }
        
        return precautions.get(disease, [
            'Consult a healthcare professional for proper diagnosis',
            'Get adequate rest and sleep',
            'Stay hydrated by drinking plenty of fluids',
            'Monitor symptoms and seek medical help if they worsen',
            'Follow any prescribed medications carefully'
        ])