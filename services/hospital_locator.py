import pandas as pd
import json
from utils.helpers import calculate_distance
import os

class HospitalLocator:
    def __init__(self):
        self.hospitals_df = self.load_hospitals_data()
    
    def load_hospitals_data(self):
        """Load hospitals dataset for India"""
        # Sample hospital data
        hospitals_data = [
            # Delhi hospitals
            {'name': 'AIIMS Delhi', 'city': 'Delhi', 'state': 'Delhi', 
             'speciality': 'Multi-Speciality', 'lat': 28.5670, 'lon': 77.2090,
             'address': 'Ansari Nagar, New Delhi', 'phone': '011-26588585', 'rating': 4.8},
            
            {'name': 'Apollo Hospital Delhi', 'city': 'Delhi', 'state': 'Delhi',
             'speciality': 'Multi-Speciality', 'lat': 28.5355, 'lon': 77.3910,
             'address': 'Sarita Vihar, New Delhi', 'phone': '011-26925858', 'rating': 4.7},
            
            {'name': 'Fortis Escorts Heart Institute', 'city': 'Delhi', 'state': 'Delhi',
             'speciality': 'Cardiac', 'lat': 28.5731, 'lon': 77.2231,
             'address': 'Okhla Road, New Delhi', 'phone': '011-47135000', 'rating': 4.6},
            
            # Mumbai hospitals
            {'name': 'Lilavati Hospital', 'city': 'Mumbai', 'state': 'Maharashtra',
             'speciality': 'Multi-Speciality', 'lat': 19.1222, 'lon': 72.8382,
             'address': 'Bandra West, Mumbai', 'phone': '022-26751000', 'rating': 4.6},
            
            {'name': 'Kokilaben Dhirubhai Ambani Hospital', 'city': 'Mumbai', 'state': 'Maharashtra',
             'speciality': 'Multi-Speciality', 'lat': 19.1297, 'lon': 72.8295,
             'address': 'Four Bungalows, Andheri West', 'phone': '022-30999999', 'rating': 4.7},
            
            # Bangalore hospitals
            {'name': 'Narayana Health', 'city': 'Bangalore', 'state': 'Karnataka',
             'speciality': 'Cardiac Care', 'lat': 12.9172, 'lon': 77.6226,
             'address': 'Hosur Road, Bangalore', 'phone': '080-71222222', 'rating': 4.5},
            
            {'name': 'Manipal Hospital', 'city': 'Bangalore', 'state': 'Karnataka',
             'speciality': 'Multi-Speciality', 'lat': 12.9416, 'lon': 77.7027,
             'address': 'Old Airport Road, Bangalore', 'phone': '080-25024444', 'rating': 4.6},
            
            # Chennai hospitals
            {'name': 'Apollo Hospitals Chennai', 'city': 'Chennai', 'state': 'Tamil Nadu',
             'speciality': 'Multi-Speciality', 'lat': 13.0286, 'lon': 80.2070,
             'address': 'Greams Road, Chennai', 'phone': '044-28293333', 'rating': 4.7},
            
            # Kolkata hospitals
            {'name': 'AMRI Hospital', 'city': 'Kolkata', 'state': 'West Bengal',
             'speciality': 'Multi-Speciality', 'lat': 22.5726, 'lon': 88.3639,
             'address': 'Salt Lake, Kolkata', 'phone': '033-66800000', 'rating': 4.5},
            
            # Hyderabad hospitals
            {'name': 'Yashoda Hospitals', 'city': 'Hyderabad', 'state': 'Telangana',
             'speciality': 'Multi-Speciality', 'lat': 17.3850, 'lon': 78.4867,
             'address': 'Somajiguda, Hyderabad', 'phone': '040-45674567', 'rating': 4.6},
            
            # Ahmedabad hospitals
            {'name': 'Apollo Hospitals Ahmedabad', 'city': 'Ahmedabad', 'state': 'Gujarat',
             'speciality': 'Multi-Speciality', 'lat': 23.0225, 'lon': 72.5714,
             'address': 'Bhat, Ahmedabad', 'phone': '079-66701800', 'rating': 4.6},
            
            # Pune hospitals
            {'name': 'Ruby Hall Clinic', 'city': 'Pune', 'state': 'Maharashtra',
             'speciality': 'Multi-Speciality', 'lat': 18.5204, 'lon': 73.8567,
             'address': 'Sassoon Road, Pune', 'phone': '020-66455555', 'rating': 4.5},
            
            # Chandigarh hospitals
            {'name': 'PGIMER', 'city': 'Chandigarh', 'state': 'Chandigarh',
             'speciality': 'Multi-Speciality', 'lat': 30.7333, 'lon': 76.7794,
             'address': 'Sector 12, Chandigarh', 'phone': '0172-274758', 'rating': 4.7},
        ]
        
        return pd.DataFrame(hospitals_data)
    
    def find_nearby_hospitals(self, user_lat, user_lon, radius_km=50, max_results=10):
        """Find hospitals within specified radius"""
        if self.hospitals_df.empty:
            return []
        
        hospitals = []
        for _, hospital in self.hospitals_df.iterrows():
            try:
                distance = calculate_distance(
                    user_lat, user_lon, 
                    hospital['lat'], hospital['lon']
                )
                if distance <= radius_km:
                    hospital_data = hospital.to_dict()
                    hospital_data['distance_km'] = round(distance, 2)
                    hospitals.append(hospital_data)
            except Exception as e:
                print(f"Error calculating distance: {e}")
                continue
        
        # Sort by distance
        hospitals.sort(key=lambda x: x['distance_km'])
        return hospitals[:max_results]
    
    def search_hospitals(self, city=None, state=None, speciality=None):
        """Search hospitals by filters"""
        results = self.hospitals_df.copy()
        
        if city:
            results = results[results['city'].str.contains(city, case=False, na=False)]
        if state:
            results = results[results['state'].str.contains(state, case=False, na=False)]
        if speciality:
            results = results[results['speciality'].str.contains(speciality, case=False, na=False)]
        
        return results.to_dict('records')