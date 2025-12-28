#!/usr/bin/env python3
"""
Flight Price Scheduler - Automatically checks prices at regular intervals
"""

import schedule
import time
from datetime import datetime
from flight_tracker import FlightTracker

def check_all_flights():
    """Check prices for all tracked flights"""
    print("\n" + "="*60)
    print(f"🔄 Starting price check at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    tracker = FlightTracker()
    flights = tracker.get_all_flights()
    
    if not flights:
        print("📭 No flights to check. Add flights using flight_cli.py")
        return
    
    print(f"✈️  Checking {len(flights)} flight(s)...\n")
    
    for flight in flights:
        flight_id = flight[0]
        origin = flight[1]
        destination = flight[2]
        departure_date = flight[3]
        
        print(f"🔍 Checking Flight #{flight_id}: {origin} → {destination} on {departure_date}")
        
        try:
            current_price = tracker.check_price(flight_id)
            
            if current_price:
                print(f"✅ Current price: ₹{current_price}\n")
            else:
                print(f"⚠️  Could not fetch price\n")
                
        except Exception as e:
            print(f"❌ Error checking flight #{flight_id}: {e}\n")
        
        # Wait 2 seconds between flights to avoid rate limiting
        time.sleep(2)
    
    print("="*60)
    print(f"✅ Price check completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"⏰ Next check in 6 hours")
    print("="*60 + "\n")

def main():
    """Main scheduler function"""
    print("\n" + "="*60)
    print("🚀 Flight Price Tracker - Automated Monitoring")
    print("="*60)
    print("⏰ Checking prices every 6 hours")
    print("📧 Email alerts enabled for price drops")
    print("🛑 Press Ctrl+C to stop")
    print("="*60 + "\n")
    
    # Run immediately on start
    check_all_flights()
    
    # Schedule to run every 6 hours
    schedule.every(6).hours.do(check_all_flights)
    
    # You can also schedule specific times:
    # schedule.every().day.at("09:00").do(check_all_flights)
    # schedule.every().day.at("15:00").do(check_all_flights)
    # schedule.every().day.at("21:00").do(check_all_flights)
    
    # Keep running
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute if a job needs to run
    except KeyboardInterrupt:
        print("\n\n🛑 Scheduler stopped by user")
        print("👋 Goodbye!\n")

if __name__ == "__main__":
    main()