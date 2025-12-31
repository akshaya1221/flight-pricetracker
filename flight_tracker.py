from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import sqlite3
from datetime import datetime
import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables
load_dotenv()

class FlightTracker:
    def __init__(self, db_path='flights.db'):
        """Initialize the flight tracker"""
        self.db_path = db_path
        self.init_database()
        
        # Email configuration
        self.email_address = os.getenv('EMAIL_ADDRESS')
        self.email_password = os.getenv('EMAIL_PASSWORD')
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        
        print(f"📧 Email configured: {self.email_address}")
    
    def init_database(self):
        """Initialize SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create flights table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS flights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                origin TEXT NOT NULL,
                destination TEXT NOT NULL,
                departure_date TEXT NOT NULL,
                email TEXT NOT NULL,
                target_price REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create price history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS price_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                flight_id INTEGER NOT NULL,
                price REAL NOT NULL,
                checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (flight_id) REFERENCES flights(id)
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Database initialized")
    
    def get_chrome_driver(self):
        """Initialize Chrome driver with proper options for PythonAnywhere"""
        chrome_options = Options()
        
        # Essential options for headless mode
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-software-rasterizer')
        chrome_options.add_argument('--disable-extensions')
        
        # User agent to avoid detection
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # Performance optimizations
        chrome_options.add_argument('--blink-settings=imagesEnabled=false')  # Don't load images
        chrome_options.page_load_strategy = 'eager'  # Don't wait for all resources
        
        try:
            # Try to use ChromeDriverManager
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            print("✅ Chrome driver initialized with ChromeDriverManager")
        except Exception as e:
            print(f"⚠️ ChromeDriverManager failed: {e}")
            # Fallback: try system chromedriver
            try:
                driver = webdriver.Chrome(options=chrome_options)
                print("✅ Chrome driver initialized with system chromedriver")
            except Exception as e2:
                print(f"❌ Could not initialize Chrome driver: {e2}")
                raise
        
        return driver
    
    def add_flight(self, origin, destination, departure_date, email, target_price=None):
        """Add a new flight to track"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO flights (origin, destination, departure_date, email, target_price)
            VALUES (?, ?, ?, ?, ?)
        ''', (origin, destination, departure_date, email, target_price))
        
        flight_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        print(f"✅ Flight added: {origin} → {destination} on {departure_date} (ID: {flight_id})")
        return flight_id
    
    def get_all_flights(self):
        """Get all tracked flights"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM flights ORDER BY created_at DESC')
        flights = cursor.fetchall()
        
        conn.close()
        return flights
    
    def delete_flight(self, flight_id):
        """Delete a flight from tracking"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Delete price history first
        cursor.execute('DELETE FROM price_history WHERE flight_id = ?', (flight_id,))
        
        # Delete flight
        cursor.execute('DELETE FROM flights WHERE id = ?', (flight_id,))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Flight {flight_id} deleted")
    
    def check_price(self, flight_id):
        """Check current price for a flight"""
        # Get flight details
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM flights WHERE id = ?', (flight_id,))
        flight = cursor.fetchone()
        
        if not flight:
            conn.close()
            raise ValueError(f"Flight {flight_id} not found")
        
        origin, destination, departure_date, email, target_price = flight[1:6]
        
        print(f"🔍 Checking price for: {origin} → {destination} on {departure_date}")
        
        driver = None
        try:
            # Initialize browser
            driver = self.get_chrome_driver()
            
            # Build Google Flights URL
            url = f"https://www.google.com/travel/flights?q=flights+from+{origin}+to+{destination}+on+{departure_date}"
            
            print(f"🌐 Opening: {url}")
            driver.get(url)
            
            # Wait for price elements to load
            wait = WebDriverWait(driver, 20)
            
            # Try multiple selectors for price
            price_selectors = [
                "div[class*='YMlIz FpEdX']",
                "div[class*='airline-price']",
                "span[class*='price']",
                "[aria-label*='price']"
            ]
            
            current_price = None
            
            for selector in price_selectors:
                try:
                    price_element = wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    price_text = price_element.text
                    
                    # Extract numeric value
                    price_str = ''.join(filter(str.isdigit, price_text))
                    if price_str:
                        current_price = float(price_str)
                        print(f"💰 Found price: ₹{current_price}")
                        break
                except:
                    continue
            
            if current_price is None:
                print("⚠️ Could not find price on page")
                # Save screenshot for debugging
                try:
                    driver.save_screenshot(f'debug_flight_{flight_id}.png')
                    print(f"📸 Screenshot saved: debug_flight_{flight_id}.png")
                except:
                    pass
                return None
            
            # Save price to history
            cursor.execute('''
                INSERT INTO price_history (flight_id, price)
                VALUES (?, ?)
            ''', (flight_id, current_price))
            conn.commit()
            
            # Check if price dropped below target
            if target_price and current_price <= target_price:
                print(f"🎉 Price alert! Current: ₹{current_price}, Target: ₹{target_price}")
                self.send_email_alert(email, origin, destination, departure_date, current_price, target_price)
            
            conn.close()
            return current_price
            
        except Exception as e:
            print(f"❌ Error checking price: {e}")
            conn.close()
            raise
        finally:
            if driver:
                driver.quit()
    
    def get_price_history(self, flight_id):
        """Get price history for a flight"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT price, checked_at 
            FROM price_history 
            WHERE flight_id = ? 
            ORDER BY checked_at DESC
        ''', (flight_id,))
        
        history = cursor.fetchall()
        conn.close()
        
        return history
    
    def send_email_alert(self, recipient, origin, destination, date, current_price, target_price):
        """Send email alert when price drops"""
        if not self.email_address or not self.email_password:
            print("⚠️ Email not configured, skipping alert")
            return
        
        try:
            # Create email
            msg = MIMEMultipart()
            msg['From'] = self.email_address
            msg['To'] = recipient
            msg['Subject'] = f'✈️ Price Alert: {origin} → {destination}'
            
            body = f"""
            🎉 Great news! The flight price has dropped!
            
            Flight Details:
            • Route: {origin} → {destination}
            • Date: {date}
            • Current Price: ₹{current_price}
            • Your Target: ₹{target_price}
            • Savings: ₹{target_price - current_price}
            
            Book now before the price goes up!
            
            Happy travels! ✈️
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_address, self.email_password)
            server.send_message(msg)
            server.quit()
            
            print(f"📧 Email alert sent to {recipient}")
            
        except Exception as e:
            print(f"❌ Error sending email: {e}")