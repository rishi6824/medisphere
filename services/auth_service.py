from models.user import User
from utils.security import validate_password, validate_email

class AuthService:
    @staticmethod
    def register_user(form_data):
        """Register a new user"""
        errors = {}
        
        # Validate required fields
        required_fields = ['username', 'email', 'password', 'confirm_password', 
                          'first_name', 'last_name', 'date_of_birth', 'gender']
        
        for field in required_fields:
            if not form_data.get(field):
                errors[field] = f'{field.replace("_", " ").title()} is required'
        
        if errors:
            return None, errors
        
        # Validate email
        if not validate_email(form_data.get('email', '')):
            errors['email'] = 'Invalid email format'
        
        # Validate password
        is_valid, password_msg = validate_password(form_data.get('password', ''))
        if not is_valid:
            errors['password'] = password_msg
        
        # Check if passwords match
        if form_data.get('password') != form_data.get('confirm_password'):
            errors['confirm_password'] = 'Passwords do not match'
        
        # Check if user exists
        if User.query.filter_by(email=form_data.get('email')).first():
            errors['email'] = 'Email already registered'
        if User.query.filter_by(username=form_data.get('username')).first():
            errors['username'] = 'Username already taken'
        
        if errors:
            return None, errors
        
        # Create new user
        try:
            user = User(
                username=form_data['username'],
                email=form_data['email'],
                first_name=form_data['first_name'],
                last_name=form_data['last_name'],
                gender=form_data['gender']
            )
            user.set_password(form_data['password'])
            
            # Use the setter method to handle date conversion
            user.set_date_of_birth(str(form_data['date_of_birth']))
            
            return user, errors
            
        except ValueError as e:
            errors['date_of_birth'] = str(e)
            return None, errors
        except Exception as e:
            errors['general'] = f'Registration failed: {str(e)}'
            return None, errors
    
    @staticmethod
    def authenticate_user(email, password):
        """Authenticate user"""
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            return user, None
        return None, 'Invalid email or password'