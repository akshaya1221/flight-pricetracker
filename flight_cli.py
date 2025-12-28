#!/usr/bin/env python3
"""
Flight Tracker CLI - Command Line Interface
"""

import sys
import argparse
from tabulate import tabulate
from flight_tracker import FlightTracker

def add_flight(args):
    """Add a new flight to track"""
    tracker = FlightTracker()
    
    flight_id = tracker.add_flight(
        origin=args.origin,
        destination=args.destination,
        departure_date=args.departure,
        email=args.email,
        target_price=args.target
    )
    
    print(f"\n✅ Flight added successfully!")
    print(f"📋 Flight ID: {flight_id}")
    print(f"✈️  Route: {args.origin} → {args.destination}")
    print(f"📅 Date: {args.departure}")
    print(f"📧 Alert Email: {args.email}")
    if args.target:
        print(f"🎯 Target Price: ₹{args.target}")
    print(f"\n💡 Tip: Run 'python flight_cli.py check {flight_id}' to check current price")

def list_flights(args):
    """List all tracked flights"""
    tracker = FlightTracker()
    flights = tracker.get_all_flights()
    
    if not flights:
        print("\n📭 No flights being tracked yet.")
        print("💡 Add one with: python flight_cli.py add --origin DEL --destination BOM --departure 2025-02-15 --email you@email.com")
        return
    
    # Format data for table
    table_data = []
    for flight in flights:
        flight_id = flight[0]
        origin = flight[1]
        destination = flight[2]
        departure_date = flight[3]
        email = flight[4]
        target_price = f"₹{flight[5]}" if flight[5] else "None"
        created_at = flight[6]
        
        table_data.append([
            flight_id,
            f"{origin} → {destination}",
            departure_date,
            email,
            target_price,
            created_at
        ])
    
    headers = ["ID", "Route", "Departure", "Email", "Target Price", "Added On"]
    print("\n" + "="*100)
    print("✈️  YOUR TRACKED FLIGHTS")
    print("="*100)
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    print(f"\n📊 Total flights tracked: {len(flights)}")

def check_price(args):
    """Check current price for a flight"""
    tracker = FlightTracker()
    
    print(f"\n🔍 Checking price for Flight ID: {args.flight_id}")
    print("⏳ This may take 10-15 seconds...\n")
    
    current_price = tracker.check_price(args.flight_id)
    
    if current_price:
        print(f"\n✅ Current Price: ₹{current_price}")
    else:
        print(f"\n❌ Could not fetch price. Flight ID might not exist.")

def price_history(args):
    """Show price history for a flight"""
    tracker = FlightTracker()
    history = tracker.get_price_history(args.flight_id)
    
    if not history:
        print(f"\n📭 No price history found for Flight ID: {args.flight_id}")
        return
    
    print(f"\n📈 Price History for Flight ID: {args.flight_id}")
    print("="*60)
    
    table_data = []
    for i, (price, checked_at) in enumerate(history, 1):
        table_data.append([i, f"₹{price}", checked_at])
    
    headers = ["#", "Price", "Checked At"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    if len(history) > 1:
        latest_price = history[0][0]
        oldest_price = history[-1][0]
        change = latest_price - oldest_price
        
        if change < 0:
            print(f"\n📉 Price decreased by ₹{abs(change)} ({abs(change/oldest_price*100):.1f}%)")
        elif change > 0:
            print(f"\n📈 Price increased by ₹{change} ({change/oldest_price*100:.1f}%)")
        else:
            print(f"\n➡️  Price unchanged")

def main():
    parser = argparse.ArgumentParser(
        description="✈️ Flight Price Tracker - Monitor flight prices and get alerts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add a flight to track
  python flight_cli.py add --origin DEL --destination BOM --departure 2025-02-15 --email you@email.com
  
  # Add with target price
  python flight_cli.py add --origin DEL --destination BOM --departure 2025-02-15 --email you@email.com --target 5000
  
  # List all tracked flights
  python flight_cli.py list
  
  # Check current price
  python flight_cli.py check 1
  
  # View price history
  python flight_cli.py history 1
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add flight command
    add_parser = subparsers.add_parser('add', help='Add a new flight to track')
    add_parser.add_argument('--origin', required=True, help='Origin airport code (e.g., DEL)')
    add_parser.add_argument('--destination', required=True, help='Destination airport code (e.g., BOM)')
    add_parser.add_argument('--departure', required=True, help='Departure date (YYYY-MM-DD)')
    add_parser.add_argument('--email', required=True, help='Email for alerts')
    add_parser.add_argument('--target', type=float, help='Target price (optional)')
    add_parser.set_defaults(func=add_flight)
    
    # List flights command
    list_parser = subparsers.add_parser('list', help='List all tracked flights')
    list_parser.set_defaults(func=list_flights)
    
    # Check price command
    check_parser = subparsers.add_parser('check', help='Check current price for a flight')
    check_parser.add_argument('flight_id', type=int, help='Flight ID to check')
    check_parser.set_defaults(func=check_price)
    
    # Price history command
    history_parser = subparsers.add_parser('history', help='View price history for a flight')
    history_parser.add_argument('flight_id', type=int, help='Flight ID')
    history_parser.set_defaults(func=price_history)
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Execute command
    args.func(args)

if __name__ == "__main__":
    main()