#!/usr/bin/env python3
import os
import sys

def setup_project():
    """Setup the project structure"""
    
    # Create necessary directories
    directories = [
        'templates/auth',
        'static/css',
        'static/js',
        'static/images',
        'static/uploads',
        'models',
        'services',
        'utils',
        'data'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")
    
    # Create empty __init__.py files
    init_files = ['models/__init__.py', 'services/__init__.py', 'utils/__init__.py']
    
    for init_file in init_files:
        with open(init_file, 'w') as f:
            f.write('# Package initialization\n')
        print(f"Created: {init_file}")
    
    print("\nProject structure created successfully!")
    print("\nNext steps:")
    print("1. Run: python app.py")
    print("2. Open http://localhost:5000 in your browser")
    print("3. Register a new account and start using Medisphere")

if __name__ == '__main__':
    setup_project()