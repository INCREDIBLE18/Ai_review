"""
Simple test script to verify the setup is correct.
Run this before deploying to check if everything is configured properly.
"""

import os
import json
from pathlib import Path

def test_imports():
    """Test if all required packages can be imported"""
    print("Testing imports...")
    try:
        import flask
        print("✓ Flask imported successfully")
    except ImportError:
        print("✗ Flask not found. Run: pip install -r requirements.txt")
        return False
    
    try:
        import flask_cors
        print("✓ flask-cors imported successfully")
    except ImportError:
        print("✗ flask-cors not found. Run: pip install -r requirements.txt")
        return False
    
    try:
        import google.generativeai
        print("✓ google-generativeai imported successfully")
    except ImportError:
        print("✗ google-generativeai not found. Run: pip install -r requirements.txt")
        return False
    
    try:
        import dotenv
        print("✓ python-dotenv imported successfully")
    except ImportError:
        print("✗ python-dotenv not found. Run: pip install -r requirements.txt")
        return False
    
    return True

def test_files():
    """Test if all required files exist"""
    print("\nTesting file structure...")
    required_files = [
        'app.py',
        'requirements.txt',
        'static/user_dashboard.html',
        'static/admin_dashboard.html',
        'README.md'
    ]
    
    all_exist = True
    for file in required_files:
        if Path(file).exists():
            print(f"✓ {file} exists")
        else:
            print(f"✗ {file} missing")
            all_exist = False
    
    return all_exist

def test_env():
    """Test environment variable setup"""
    print("\nTesting environment setup...")
    
    # Check if .env file exists
    if Path('.env').exists():
        print("✓ .env file exists")
    else:
        print("⚠ .env file not found (create it with GEMINI_API_KEY)")
    
    # Check if API key is set
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('GEMINI_API_KEY', '')
    if api_key:
        print("✓ GEMINI_API_KEY is set")
        return True
    else:
        print("⚠ GEMINI_API_KEY not set (required for AI features)")
        print("  Create .env file with: GEMINI_API_KEY=your_key_here")
        return False

def test_data_file():
    """Test data file initialization"""
    print("\nTesting data storage...")
    data_file = 'feedback_data.json'
    
    if Path(data_file).exists():
        try:
            with open(data_file, 'r') as f:
                data = json.load(f)
            print(f"✓ {data_file} exists and is valid JSON ({len(data)} entries)")
        except json.JSONDecodeError:
            print(f"✗ {data_file} exists but is not valid JSON")
            return False
    else:
        print(f"✓ {data_file} will be created on first run")
    
    return True

def main():
    print("=" * 50)
    print("AI Feedback System - Setup Test")
    print("=" * 50)
    
    results = []
    results.append(("Imports", test_imports()))
    results.append(("Files", test_files()))
    results.append(("Environment", test_env()))
    results.append(("Data Storage", test_data_file()))
    
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{name}: {status}")
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        print("\n✓ All tests passed! You're ready to run the application.")
        print("\nTo start the app, run:")
        print("  python app.py")
    else:
        print("\n⚠ Some tests failed. Please fix the issues above.")
    
    return all_passed

if __name__ == '__main__':
    main()

