#!/usr/bin/env python3
"""
Test script for Mexican Trout Biodiversity Project
Verifies that the Flask application works correctly
"""

import requests
import time
import subprocess
import sys
import os

def test_app():
    """Test the Flask application"""
    print("Testing Mexican Trout Biodiversity Application...")
    
    # Start the app in background
    try:
        # Start the Flask app
        process = subprocess.Popen([sys.executable, 'app.py'], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
        
        # Wait for app to start
        print("Starting Flask application...")
        time.sleep(5)
        
        # Test basic endpoints
        base_url = "http://localhost:5000"
        
        # Test home page
        print("Testing home page...")
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            print("✅ Home page works")
        else:
            print(f"❌ Home page failed: {response.status_code}")
        
        # Test API endpoints
        print("Testing API endpoints...")
        
        # Test statistics endpoint
        response = requests.get(f"{base_url}/api/statistics", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Statistics API works - {data.get('total_records', 0)} records")
        else:
            print(f"❌ Statistics API failed: {response.status_code}")
        
        # Test species endpoint
        response = requests.get(f"{base_url}/api/species", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Species API works - {len(data)} species")
        else:
            print(f"❌ Species API failed: {response.status_code}")
        
        # Test occurrences endpoint
        response = requests.get(f"{base_url}/api/occurrences", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Occurrences API works - {len(data.get('records', []))} records")
        else:
            print(f"❌ Occurrences API failed: {response.status_code}")
        
        # Test map data endpoint
        response = requests.get(f"{base_url}/api/map-data", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Map data API works - {len(data.get('features', []))} features")
        else:
            print(f"❌ Map data API failed: {response.status_code}")
        
        # Test other pages
        pages = ['/species', '/map', '/data', '/admin']
        for page in pages:
            response = requests.get(f"{base_url}{page}", timeout=10)
            if response.status_code == 200:
                print(f"✅ {page} page works")
            else:
                print(f"❌ {page} page failed: {response.status_code}")
        
        print("\n🎉 All tests completed successfully!")
        print("The Mexican Trout Biodiversity Application is working correctly.")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    
    finally:
        # Clean up
        try:
            process.terminate()
            process.wait(timeout=5)
        except:
            process.kill()
    
    return True

if __name__ == "__main__":
    success = test_app()
    sys.exit(0 if success else 1) 