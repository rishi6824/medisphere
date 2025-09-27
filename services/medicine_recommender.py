import json
import os

class MedicineRecommender:
    def __init__(self):
        self.medicines_data = self.load_medicines_data()
    
    def load_medicines_data(self):
        """Load medicine database"""
        medicines = {
            'Common Cold': [
                {'name': 'Paracetamol', 'type': 'Tablet', 'dosage': '500mg', 'frequency': 'Every 6 hours as needed for fever/pain'},
                {'name': 'Chlorpheniramine', 'type': 'Tablet', 'dosage': '4mg', 'frequency': 'Every 8 hours for allergies'},
                {'name': 'Vitamin C', 'type': 'Tablet', 'dosage': '500-1000mg', 'frequency': 'Once daily'},
                {'name': 'Zinc Lozenges', 'type': 'Lozenge', 'dosage': '10-15mg', 'frequency': 'Every 2-3 hours as needed'}
            ],
            'Influenza (Flu)': [
                {'name': 'Oseltamivir (Tamiflu)', 'type': 'Capsule', 'dosage': '75mg', 'frequency': 'Twice daily for 5 days'},
                {'name': 'Ibuprofen', 'type': 'Tablet', 'dosage': '200-400mg', 'frequency': 'Every 6-8 hours as needed'},
                {'name': 'Paracetamol', 'type': 'Tablet', 'dosage': '500mg', 'frequency': 'Every 6 hours as needed'},
                {'name': 'Decongestants', 'type': 'Tablet/Spray', 'dosage': 'As directed', 'frequency': 'As needed for congestion'}
            ],
            'COVID-19': [
                {'name': 'Paracetamol', 'type': 'Tablet', 'dosage': '500mg', 'frequency': 'Every 6 hours for fever/pain'},
                {'name': 'Vitamin C', 'type': 'Tablet', 'dosage': '1000mg', 'frequency': 'Once daily'},
                {'name': 'Zinc', 'type': 'Tablet', 'dosage': '50mg', 'frequency': 'Once daily'},
                {'name': 'Vitamin D3', 'type': 'Tablet', 'dosage': '1000-2000 IU', 'frequency': 'Once daily'}
            ],
            'Migraine': [
                {'name': 'Sumatriptan', 'type': 'Tablet', 'dosage': '50-100mg', 'frequency': 'At migraine onset, max 200mg/day'},
                {'name': 'Ibuprofen', 'type': 'Tablet', 'dosage': '400-600mg', 'frequency': 'At onset, every 6 hours as needed'},
                {'name': 'Propranolol', 'type': 'Tablet', 'dosage': '40-80mg', 'frequency': 'Twice daily (preventive)'},
                {'name': 'Anti-nausea medication', 'type': 'Tablet', 'dosage': 'As prescribed', 'frequency': 'As needed'}
            ],
            'Food Poisoning': [
                {'name': 'Oral Rehydration Solution (ORS)', 'type': 'Powder', 'dosage': '1 packet in 1L water', 'frequency': 'After each loose motion'},
                {'name': 'Loperamide', 'type': 'Tablet', 'dosage': '2mg', 'frequency': 'After each loose motion, max 8mg/day'},
                {'name': 'Paracetamol', 'type': 'Tablet', 'dosage': '500mg', 'frequency': 'Every 6 hours for pain/fever'},
                {'name': 'Probiotics', 'type': 'Capsule', 'dosage': 'As directed', 'frequency': 'Once or twice daily'}
            ],
            'Allergies': [
                {'name': 'Cetirizine', 'type': 'Tablet', 'dosage': '10mg', 'frequency': 'Once daily'},
                {'name': 'Loratadine', 'type': 'Tablet', 'dosage': '10mg', 'frequency': 'Once daily'},
                {'name': 'Antihistamine Nasal Spray', 'type': 'Spray', 'dosage': '1-2 sprays/nostril', 'frequency': 'Twice daily'},
                {'name': 'Decongestants', 'type': 'Tablet', 'dosage': 'As directed', 'frequency': 'As needed'}
            ]
        }
        return medicines
    
    def recommend_medicines(self, disease):
        """Recommend medicines for diagnosed disease"""
        return self.medicines_data.get(disease, [
            {'name': 'Consult Healthcare Professional', 'type': 'Medical Advice', 'dosage': 'N/A', 'frequency': 'Immediately'},
            {'name': 'Rest and Hydration', 'type': 'General Care', 'dosage': 'N/A', 'frequency': 'Continuous'},
            {'name': 'Symptom Monitoring', 'type': 'Self-Care', 'dosage': 'N/A', 'frequency': 'Regular checks'}
        ])
    
    def get_medicine_details(self, medicine_name):
        """Get detailed information about a specific medicine"""
        medicine_db = {
            'Paracetamol': {
                'description': 'Pain reliever and fever reducer. Also known as acetaminophen.',
                'side_effects': 'Rare when taken as directed. Overdose can cause liver damage.',
                'precautions': 'Do not exceed 4000mg per day. Avoid alcohol. Consult doctor for liver problems.',
                'interactions': 'May interact with warfarin and other blood thinners.'
            },
            'Ibuprofen': {
                'description': 'Nonsteroidal anti-inflammatory drug (NSAID) for pain, fever, and inflammation.',
                'side_effects': 'Stomach upset, heartburn, dizziness. Rare but serious: stomach bleeding.',
                'precautions': 'Take with food. Avoid if pregnant or have kidney/heart problems.',
                'interactions': 'May interact with aspirin, blood thinners, and certain blood pressure medications.'
            },
            'Cetirizine': {
                'description': 'Antihistamine used to relieve allergy symptoms.',
                'side_effects': 'Drowsiness, dry mouth, fatigue (usually mild).',
                'precautions': 'Avoid alcohol. Use caution when driving or operating machinery.',
                'interactions': 'May interact with sedatives and other CNS depressants.'
            },
            'Oseltamivir (Tamiflu)': {
                'description': 'Antiviral medication for influenza treatment and prevention.',
                'side_effects': 'Nausea, vomiting, headache. Usually mild and temporary.',
                'precautions': 'Start within 48 hours of symptom onset for best效果.',
                'interactions': 'Limited significant drug interactions.'
            }
        }
        return medicine_db.get(medicine_name, {
            'description': 'Consult package insert or healthcare provider for detailed information.',
            'side_effects': 'Vary by medication. Always read instructions carefully.',
            'precautions': 'Follow dosage instructions. Consult doctor for underlying conditions.',
            'interactions': 'Discuss all medications with your healthcare provider.'
        })