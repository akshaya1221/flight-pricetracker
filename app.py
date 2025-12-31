from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flight_tracker import FlightTracker
import os
import traceback

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'flight-tracker-secret-key-2025')

# Initialize tracker
tracker = None
try:
    tracker = FlightTracker()
    print("✅ Flight Tracker initialized successfully")
except Exception as e:
    print(f"❌ Error initializing tracker: {e}")
    traceback.print_exc()

@app.route('/')
def index():
    """Home page - shows all tracked flights"""
    try:
        if tracker is None:
            return render_template('error.html', 
                                 error="Flight Tracker could not be initialized. Please check configuration.")
        
        flights = tracker.get_all_flights()
        return render_template('index.html', flights=flights)
    except Exception as e:
        print(f"❌ Error loading flights: {e}")
        traceback.print_exc()
        return render_template('error.html', error=str(e))

@app.route('/add', methods=['GET', 'POST'])
def add_flight():
    """Add new flight page"""
    if tracker is None:
        flash('⚠️ Tracker is currently unavailable. Please try again later.', 'warning')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        try:
            # Get form data
            origin = request.form.get('origin', '').strip().upper()
            destination = request.form.get('destination', '').strip().upper()
            departure_date = request.form.get('departure_date', '').strip()
            email = request.form.get('email', '').strip()
            target_price = request.form.get('target_price', '').strip()
            
            print(f"📝 Form data received:")
            print(f"   Origin: {origin}")
            print(f"   Destination: {destination}")
            print(f"   Date: {departure_date}")
            print(f"   Email: {email}")
            print(f"   Target: {target_price}")
            
            # Validate inputs
            if not origin or not destination or not departure_date or not email:
                flash('❌ Please fill in all required fields!', 'error')
                return redirect(url_for('add_flight'))
            
            if len(origin) != 3 or len(destination) != 3:
                flash('❌ Airport codes must be exactly 3 letters!', 'error')
                return redirect(url_for('add_flight'))
            
            # Convert target price to float if provided
            if target_price:
                try:
                    target_price = float(target_price)
                except ValueError:
                    flash('❌ Target price must be a valid number!', 'error')
                    return redirect(url_for('add_flight'))
            else:
                target_price = None
            
            # Add flight to tracker
            flight_id = tracker.add_flight(
                origin=origin,
                destination=destination,
                departure_date=departure_date,
                email=email,
                target_price=target_price
            )
            
            print(f"✅ Flight added successfully! ID: {flight_id}")
            flash(f'✅ Flight added successfully! Tracking {origin} → {destination}', 'success')
            return redirect(url_for('index'))
            
        except Exception as e:
            print(f"❌ Error adding flight: {e}")
            traceback.print_exc()
            flash(f'❌ Error adding flight: {str(e)}', 'error')
            return redirect(url_for('add_flight'))
    
    # GET request - show form
    return render_template('add_flight.html')

@app.route('/check/<int:flight_id>')
def check_flight(flight_id):
    """Check price for a specific flight"""
    if tracker is None:
        flash('⚠️ Tracker is currently unavailable.', 'warning')
        return redirect(url_for('index'))
    
    try:
        print(f"🔍 Checking price for flight ID: {flight_id}")
        current_price = tracker.check_price(flight_id)
        
        if current_price:
            flash(f'✅ Current price: ₹{current_price}', 'success')
        else:
            flash('⚠️ Could not fetch price. Please try again later.', 'warning')
    except Exception as e:
        print(f"❌ Error checking flight: {e}")
        traceback.print_exc()
        flash(f'❌ Error: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/delete/<int:flight_id>')
def delete_flight(flight_id):
    """Delete a tracked flight"""
    if tracker is None:
        flash('⚠️ Tracker is currently unavailable.', 'warning')
        return redirect(url_for('index'))
    
    try:
        tracker.delete_flight(flight_id)
        flash(f'✅ Flight deleted successfully!', 'success')
    except Exception as e:
        print(f"❌ Error deleting flight: {e}")
        flash(f'❌ Error: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/history/<int:flight_id>')
def price_history(flight_id):
    """View price history for a flight"""
    if tracker is None:
        flash('⚠️ Tracker is currently unavailable.', 'warning')
        return redirect(url_for('index'))
    
    try:
        history = tracker.get_price_history(flight_id)
        
        # Get flight details
        flights = tracker.get_all_flights()
        flight = next((f for f in flights if f[0] == flight_id), None)
        
        if flight is None:
            flash('❌ Flight not found!', 'error')
            return redirect(url_for('index'))
        
        return render_template('history.html', history=history, flight=flight, flight_id=flight_id)
    except Exception as e:
        print(f"❌ Error loading history: {e}")
        traceback.print_exc()
        flash(f'❌ Error: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/api/flights')
def api_flights():
    """API endpoint to get all flights as JSON"""
    if tracker is None:
        return jsonify({'error': 'Tracker is currently unavailable', 'flights': []}), 503
    
    try:
        flights = tracker.get_all_flights()
        flights_data = []
        
        for flight in flights:
            flights_data.append({
                'id': flight[0],
                'origin': flight[1],
                'destination': flight[2],
                'departure_date': flight[3],
                'email': flight[4],
                'target_price': flight[5],
                'created_at': flight[6]
            })
        
        return jsonify(flights_data)
    except Exception as e:
        print(f"❌ API Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy' if tracker is not None else 'degraded',
        'service': 'flight-price-tracker',
        'tracker_enabled': tracker is not None
    }), 200

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    port = int(os.environ.get('PORT', 5000))
    
    print("\n" + "="*70)
    print("🚀 Flight Price Tracker Starting...")
    print("="*70)
    print(f"📱 Server: http://localhost:{port}")
    print(f"🔧 Tracker Status: {'✅ Enabled' if tracker else '❌ Disabled'}")
    print("🛑 Press Ctrl+C to stop")
    print("="*70 + "\n")
    
    app.run(debug=False, host='0.0.0.0', port=port)