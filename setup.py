#!/usr/bin/env python3
"""
Setup script for Mexican Trout Biodiversity Project
Automates the installation and setup process
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version}")
    return True

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def create_database():
    """Create the database and tables"""
    print("Creating database...")
    try:
        from app import app, db
        with app.app_context():
            db.create_all()
        print("✅ Database created successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to create database: {e}")
        return False

def create_env_file():
    """Create .env file from template"""
    if not os.path.exists('.env'):
        print("Creating .env file...")
        try:
            shutil.copy('env_example.txt', '.env')
            print("✅ .env file created from template")
            print("⚠️  Please edit .env file with your configuration")
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    else:
        print("✅ .env file already exists")
    return True

def test_import_script():
    """Test the data import script"""
    print("Testing data import script...")
    try:
        # Just test if the script can be imported
        from import_data import load_excel_data, clean_data
        print("✅ Import script is working")
        return True
    except Exception as e:
        print(f"❌ Import script test failed: {e}")
        return False

def run_tests():
    """Run application tests"""
    print("Running application tests...")
    try:
        subprocess.check_call([sys.executable, "test_app.py"])
        print("✅ All tests passed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Tests failed: {e}")
        return False

def main():
    """Main setup function"""
    print("=" * 60)
    print("Mexican Trout Biodiversity Project - Setup")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install requirements
    if not install_requirements():
        return False
    
    # Create environment file
    if not create_env_file():
        return False
    
    # Create database
    if not create_database():
        return False
    
    # Test import script
    if not test_import_script():
        return False
    
    # Run tests
    if not run_tests():
        return False
    
    print("\n" + "=" * 60)
    print("🎉 Setup completed successfully!")
    print("=" * 60)
    
    print("\nNext steps:")
    print("1. Edit .env file with your configuration")
    print("2. Run: python app.py")
    print("3. Open: http://localhost:5000")
    print("4. Import data: python import_data.py")
    
    print("\nFor help, see README.md")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 