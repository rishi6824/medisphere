import re
import random
from datetime import datetime

class ChatbotEngine:
    def __init__(self):
        self.responses = self.load_responses()
    
    def load_responses(self):
        """Load chatbot responses and patterns"""
        return {
            'greetings': {
                'patterns': ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening'],
                'responses': [
                    "Hello! I'm Medibot, your medical assistant. How can I help you today?",
                    "Hi there! How can I assist you with your health concerns?",
                    "Hello! I'm here to help with medical information. What would you like to know?",
                    "Greetings! I'm your healthcare assistant. How can I support you today?"
                ]
            },
            'symptoms': {
                'patterns': ['symptom', 'pain', 'hurt', 'fever', 'cough', 'headache', 'ache', 'unwell', 'sick'],
                'responses': [
                    "I understand you're experiencing symptoms. For accurate diagnosis, please use our symptom checker feature on the diagnosis page.",
                    "I can help guide you, but for specific symptoms, our AI diagnosis tool can provide better insights and recommendations.",
                    "Please describe your symptoms in detail, or visit the diagnosis section for a comprehensive analysis.",
                    "Symptoms can indicate various conditions. Our diagnosis system can help identify potential causes based on your symptoms."
                ]
            },
            'medicines': {
                'patterns': ['medicine', 'pill', 'tablet', 'dosage', 'prescription', 'drug', 'medication'],
                'responses': [
                    "I can provide general medicine information. For specific prescriptions, please consult a doctor or use our medicine database.",
                    "Medicine recommendations are available in our diagnosis results. Always consult a doctor before taking new medications.",
                    "You can search for medicine information in our database. Remember, I'm not a substitute for professional medical advice.",
                    "For detailed medicine information, check our medicines section. Important: Always follow professional medical guidance."
                ]
            },
            'emergency': {
                'patterns': ['emergency', 'help', 'urgent', 'serious', 'critical', '911', 'ambulance'],
                'responses': [
                    "🚨 If this is a medical emergency, please call your local emergency number immediately!",
                    "For urgent medical issues, please contact emergency services or visit the nearest hospital right away.",
                    "This sounds serious. Please seek immediate medical attention if you're experiencing an emergency.",
                    "Emergency situations require immediate professional help. Please call emergency services now!"
                ]
            },
            'general_health': {
                'patterns': ['health', 'diet', 'exercise', 'sleep', 'fitness', 'healthy', 'wellness'],
                'responses': [
                    "Maintaining good health involves balanced diet, regular exercise, adequate sleep, and stress management.",
                    "A healthy lifestyle includes proper nutrition, physical activity, good sleep habits, and regular check-ups.",
                    "Good health practices involve balanced eating, staying active, getting enough rest, and managing stress effectively.",
                    "Health maintenance requires consistent habits: nutritious food, regular exercise, quality sleep, and preventive care."
                ]
            },
            'appointment': {
                'patterns': ['appointment', 'doctor', 'consult', 'visit', 'schedule'],
                'responses': [
                    "You can find nearby hospitals and contact them directly for appointments using our hospital locator.",
                    "For doctor appointments, please contact healthcare facilities directly. Our hospital finder can help you locate nearby options.",
                    "Use our hospital directory to find healthcare providers and schedule appointments as needed.",
                    "I recommend using our hospital search feature to find medical facilities where you can book appointments."
                ]
            },
            'thanks': {
                'patterns': ['thank', 'thanks', 'appreciate', 'grateful'],
                'responses': [
                    "You're welcome! I'm glad I could help. Take care of your health!",
                    "You're welcome! Feel free to ask if you have more questions about your health.",
                    "Happy to help! Remember to consult healthcare professionals for serious concerns.",
                    "You're welcome! Stay healthy and don't hesitate to reach out if you need more information."
                ]
            },
            'fallback': {
                'responses': [
                    "I'm still learning about medical topics. Could you rephrase your question?",
                    "I understand you're asking about healthcare. For specific concerns, please use our diagnosis tools or consult a professional.",
                    "I'm here to help with medical information. Could you provide more details about your question?",
                    "For accurate medical advice, I recommend consulting with our AI diagnosis system or a healthcare professional.",
                    "I specialize in general health information. For detailed medical advice, please use our specialized tools or consult a doctor."
                ]
            }
        }
    
    def classify_intent(self, message):
        """Classify user intent from message"""
        message_lower = message.lower()
        
        for intent, data in self.responses.items():
            if intent == 'fallback':
                continue
            for pattern in data['patterns']:
                if re.search(r'\b' + re.escape(pattern) + r'\b', message_lower):
                    return intent
        
        return 'fallback'
    
    def generate_response(self, message):
        """Generate response to user message"""
        intent = self.classify_intent(message)
        responses = self.responses[intent]['responses']
        
        # Add contextual response for medical queries
        response = random.choice(responses)
        
        # Add disclaimer for medical advice
        if intent in ['symptoms', 'medicines', 'emergency']:
            response += "\n\n⚠️ **Disclaimer:** I'm an AI assistant and not a substitute for professional medical advice, diagnosis, or treatment."
        
        return response
    
    def is_medical_question(self, message):
        """Determine if the question is medical-related"""
        medical_keywords = [
            'pain', 'hurt', 'fever', 'cough', 'headache', 'medicine', 'pill',
            'symptom', 'disease', 'illness', 'sick', 'hospital', 'doctor',
            'emergency', 'blood', 'heart', 'lungs', 'stomach', 'infection',
            'virus', 'bacteria', 'treatment', 'diagnosis', 'health', 'medical'
        ]
        
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in medical_keywords)