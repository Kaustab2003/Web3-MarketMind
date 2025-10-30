"""
Test script to verify all dependencies are installed correctly
Run this before starting the app to ensure everything is set up properly
"""

import sys

def test_imports():
    """Test all required imports"""
    print("🔍 Testing Python version...")
    if sys.version_info < (3, 11):
        print(f"⚠️  Warning: Python {sys.version_info.major}.{sys.version_info.minor} detected. Python 3.11+ recommended.")
    else:
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} - OK")
    
    print("\n🔍 Testing required packages...")
    
    packages = [
        ("streamlit", "Streamlit"),
        ("pandas", "Pandas"),
        ("numpy", "NumPy"),
        ("plotly", "Plotly"),
        ("sklearn", "scikit-learn"),
        ("requests", "Requests"),
        ("streamlit_authenticator", "Streamlit Authenticator"),
        ("joblib", "Joblib"),
        ("fpdf", "FPDF"),
        ("seaborn", "Seaborn"),
        ("matplotlib", "Matplotlib"),
        ("dotenv", "python-dotenv"),
        ("yaml", "PyYAML"),
    ]
    
    failed = []
    
    for module_name, display_name in packages:
        try:
            __import__(module_name)
            print(f"✅ {display_name} - OK")
        except ImportError as e:
            print(f"❌ {display_name} - MISSING")
            failed.append(display_name)
    
    if failed:
        print(f"\n❌ Installation incomplete. Missing packages: {', '.join(failed)}")
        print("\n📦 To install missing packages, run:")
        print("   pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All packages installed successfully!")
        return True

def test_directories():
    """Test required directories exist"""
    import os
    
    print("\n🔍 Testing directory structure...")
    
    dirs = [
        ".streamlit",
        "models",
        "data",
    ]
    
    for dir_name in dirs:
        if os.path.exists(dir_name):
            print(f"✅ {dir_name}/ - OK")
        else:
            print(f"⚠️  {dir_name}/ - Creating...")
            os.makedirs(dir_name, exist_ok=True)
            print(f"✅ {dir_name}/ - Created")
    
    return True

def test_files():
    """Test required files exist"""
    import os
    
    print("\n🔍 Testing required files...")
    
    files = [
        ("app_v4.py", "Main application"),
        ("requirements.txt", "Dependencies"),
        (".streamlit/config.toml", "Streamlit config"),
    ]
    
    missing = []
    
    for file_path, description in files:
        if os.path.exists(file_path):
            print(f"✅ {description} ({file_path}) - OK")
        else:
            print(f"❌ {description} ({file_path}) - MISSING")
            missing.append(file_path)
    
    if missing:
        print(f"\n❌ Missing files: {', '.join(missing)}")
        return False
    
    return True

def test_secrets():
    """Check if secrets are configured"""
    import os
    
    print("\n🔍 Testing secrets configuration...")
    
    if os.path.exists(".streamlit/secrets.toml"):
        print("✅ Secrets file found (.streamlit/secrets.toml)")
    else:
        print("⚠️  Secrets file not found (.streamlit/secrets.toml)")
        print("   This is OK for demo mode, but recommended for production")
    
    # Check environment variables
    if os.getenv("DEMO_PASSWORD"):
        print("✅ DEMO_PASSWORD environment variable set")
    else:
        print("ℹ️  DEMO_PASSWORD not set (will use default)")
    
    if os.getenv("ADMIN_PASSWORD"):
        print("✅ ADMIN_PASSWORD environment variable set")
    else:
        print("ℹ️  ADMIN_PASSWORD not set (will use default)")
    
    return True

def test_api_connectivity():
    """Test API connectivity"""
    import requests
    
    print("\n🔍 Testing API connectivity...")
    
    # Test CoinGecko
    try:
        response = requests.get("https://api.coingecko.com/api/v3/ping", timeout=10)
        if response.status_code == 200:
            print("✅ CoinGecko API - Reachable")
        else:
            print(f"⚠️  CoinGecko API - Status {response.status_code}")
    except Exception as e:
        print(f"❌ CoinGecko API - Unreachable ({str(e)[:50]})")
    
    # Test Binance
    try:
        response = requests.get("https://api.binance.com/api/v3/ping", timeout=10)
        if response.status_code == 200:
            print("✅ Binance API - Reachable")
        else:
            print(f"⚠️  Binance API - Status {response.status_code}")
    except Exception as e:
        print(f"❌ Binance API - Unreachable ({str(e)[:50]})")
    
    return True

def main():
    """Run all tests"""
    print("=" * 60)
    print("  Web3 MarketMind 4.0 - Installation Test")
    print("=" * 60)
    
    results = []
    
    results.append(("Package Installation", test_imports()))
    results.append(("Directory Structure", test_directories()))
    results.append(("Required Files", test_files()))
    results.append(("Secrets Configuration", test_secrets()))
    results.append(("API Connectivity", test_api_connectivity()))
    
    print("\n" + "=" * 60)
    print("  Test Summary")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n🎉 All tests passed! You're ready to run the app.")
        print("\n📝 Next steps:")
        print("   1. Run: streamlit run app_v4.py")
        print("   2. Or use quick start: run.bat (Windows) or ./run.sh (Mac/Linux)")
        print("   3. Login with: demo / demo123")
        print("\n🌐 The app will open at: http://localhost:8501")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above before running the app.")
        print("\n📦 Common fixes:")
        print("   - Install dependencies: pip install -r requirements.txt")
        print("   - Check file paths are correct")
        print("   - Verify internet connection for API tests")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
