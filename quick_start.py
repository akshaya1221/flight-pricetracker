#!/usr/bin/env python3
"""
Quick Start Setup for Flight Price Tracker
Run this script to set up your flight tracker quickly!
"""

import os
import sys
from pathlib import Path

def print_header(text):
    """Print a nice header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def check_env_file():
    """Check if .env file exists"""
    if Path(".env").exists():
        print("✓ .env file found")
        return True
    else:
        print("✗ .env file not found")
        return False

def create_env_file():
    """Interactive .env file creation"""
    print_header("Setting Up Environment Variables")
    
    print("Let's set up your API keys and email configuration.\n")
    
    print("1. AMADEUS API KEYS")
    print("   Get them from: https://developers.amadeus.com")
    api_key = input("   Enter your Amadeus API Key: ").strip()
    api_secret = input("   Enter your Amadeus API Secret: ").strip()
    
    print("\n2. EMAIL CONFIGURATION")
    print("   For Gmail, use App Password (not regular password)")
    print("   How to get: Google Account → Security → App Passwords")
    from_email = input("   Enter your Gmail address: ").strip()
    email_password = input("   Enter your Gmail App Password: ").strip()
    
    # Create .env file
    env_content = f"""# Amadeus API Configuration
AMADEUS_API_KEY={api_key}
AMADEUS_API_SECRET={api_secret}

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
FROM_EMAIL={from_email}
EMAIL_PASSWORD={email_password}
"""
    
    with open(".env", "w") as f:
        f.write(env_content)
    
    print("\n✓ .env file created successfully!")

def test_imports():
    """Test if all required packages are installed"""
    print_header("Checking Dependencies")
    
    required_packages = {
        'requests': 'requests',
        'selenium': 'selenium',
        'pandas': 'pandas',
        'dotenv': 'python-dotenv',
        'schedule': 'schedule',
        'tabulate': 'tabulate'
    }
    
    missing = []
    
    for module, package in required_packages.items():
        try:
            __import__(module)
            print(f"✓ {package} installed")
        except ImportError:
            print(f"✗ {package} missing")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("\nInstall them with:")
        print(f"pip install {' '.join(missing)}")
        return False
    
    print("\n✓ All dependencies installed!")
    return True

def create_database():
    """Initialize the database"""
    try:
        import sqlite3
        conn = sqlite3.connect('flight_prices.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS flight_searches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                origin TEXT NOT NULL,
                destination TEXT NOT NULL,
                departure_date TEXT NOT NULL,
                return_date TEXT,
                user_email TEXT NOT NULL,
                target_price REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS price_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                search_id INTEGER,
                price REAL NOT NULL,
                currency TEXT DEFAULT 'USD',
                airline TEXT,
                checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (search_id) REFERENCES flight_searches(id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
        print("✓ Database initialized successfully!")
        return True
    except Exception as e:
        print(f"✗ Database initialization failed: {e}")
        return False

def show_next_steps():
    """Display next steps for the user"""
    print_header("Setup Complete! 🎉")
    
    print("You're ready to start tracking flights!\n")
    
    print("📚 QUICK START COMMANDS:\n")
    
    print("1. Add your first flight to track:")
    print("   python flight_cli.py add --origin DEL --destination BOM \\")
    print("       --departure 2025-02-15 --email your@email.com --target 5000\n")
    
    print("2. List all tracked flights:")
    print("   python flight_cli.py list\n")
    
    print("3. Check prices manually:")
    print("   python flight_cli.py check\n")
    
    print("4. Start automated monitoring (runs every 6 hours):")
    print("   python flight_scheduler.py\n")
    
    print("5. View price history:")
    print("   python flight_cli.py history --id 1\n")
    
    print("📖 For more information, check README.md\n")
    
    print("💡 TIP: Test with a real flight search first before scheduling!")
    print("="*60 + "\n")

def main():
    """Main setup function"""
    print("\n" + "🛫"*20)
    print_header("Flight Price Tracker - Quick Setup")
    print("🛬"*20 + "\n")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("⚠️  Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected\n")
    
    # Check dependencies
    if not test_imports():
        print("\n⚠️  Please install missing packages first:")
        print("pip install -r requirements.txt")
        return
    
    # Check/create .env file
    if not check_env_file():
        response = input("\nWould you like to create .env file now? (y/n): ")
        if response.lower() == 'y':
            create_env_file()
        else:
            print("\n⚠️  You'll need to create .env file manually.")
            print("Copy .env.example to .env and fill in your credentials.")
            return
    
    # Initialize database
    print_header("Initializing Database")
    create_database()
    
    # Show next steps
    show_next_steps()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup cancelled by user")
    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        print("Please check the error and try again.")