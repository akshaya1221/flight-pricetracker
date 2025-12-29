from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
import traceback

app = Flask(__name__)
app.secret_key = 'flight-tracker-secret-key-2025'

# Temporarily disable tracker for deployment
# Selenium won't work on Render without proper headless setup
tracker = None
print("⚠️ Tracker disabled for initial deployment")

# TODO: Configure headless Chrome for production later
# try:
#     from flight_tracker import FlightTracker
#     tracker = FlightTracker()
#     print("✅ Flight Tracker initialized successfully")
# except Exception as e:
#     print(f"❌ Error initializing tracker: {e}")
#     traceback.print_exc()

@app.route('/')
def index():
    """Home page - shows deployment status"""
    if tracker is None:
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Flight Price Tracker</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 50px auto;
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                }
                .container {
                    background: rgba(255,255,255,0.1);
                    padding: 40px;
                    border-radius: 15px;
                    backdrop-filter: blur(10px);
                }
                h1 { font-size: 2.5em; margin-bottom: 10px; }
                .status { font-size: 1.2em; margin: 20px 0; }
                .success { color: #00ff88; }
                .warning { color: #ffeb3b; }
                a {
                    color: #00ff88;
                    text-decoration: none;
                    font-weight: bold;
                }
                .info-box {
                    background: rgba(255,255,255,0.2);
                    padding: 20px;
                    border-radius: 10px;
                    margin: 20px 0;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>✈️ Flight Price Tracker</h1>
                <p class="status success">✅ Your web server is running successfully on Render!</p>
                <p class="status warning">⚠️ Tracker functionality is currently disabled for deployment testing</p>
                
                <div class="info-box">
                    <h2>🎉 Deployment Success!</h2>
                    <p>Your Flask application is live and accessible on the internet!</p>
                    <p><strong>URL:</strong> This page</p>
                    <p><strong>Status:</strong> Live and responding</p>
                </div>
                
                <div class="info-box">
                    <h2>📋 Next Steps:</h2>
                    <ul>
                        <li>✅ Flask is installed and working</li>
                        <li>✅ Gunicorn is serving the app</li>
                        <li>✅ Render deployment is successful</li>
                        <li>⏳ Configure headless Chrome for scraping (next phase)</li>
                    </ul>
                </div>
                
                <p><a href="/test">→ Test additional endpoint</a></p>
            </div>
        </body>
        </html>
        """
    
    try:
        flights = tracker.get_all_flights()
        return render_template('index.html', flights=flights)
    except Exception as e:
        print(f"❌ Error loading flights: {e}")
        traceback.print_exc()
        return f"Error: {e}", 500

@app.route('/add', methods=['GET', 'POST'])
def add_flight():
    """Add new flight page"""
    if tracker is None:
        flash('⚠️ Tracker is currently disabled. Feature coming soon!', 'warning')
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
            flash(f'✅ Flight added successfully! Tracking {origin} → {destination} (ID: {flight_id})', 'success')
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
        flash('⚠️ Tracker is currently disabled. Feature coming soon!', 'warning')
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

@app.route('/history/<int:flight_id>')
def price_history(flight_id):
    """View price history for a flight"""
    if tracker is None:
        flash('⚠️ Tracker is currently disabled. Feature coming soon!', 'warning')
        return redirect(url_for('index'))
    
    try:
        history = tracker.get_price_history(flight_id)
        
        # Get flight details
        flights = tracker.get_all_flights()
        flight = next((f for f in flights if f[0] == flight_id), None)
        
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
        return jsonify({'error': 'Tracker is currently disabled', 'flights': []}), 200
    
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

@app.route('/test')
def test():
    """Test page to check if Flask is working"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Page</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 600px;
                margin: 50px auto;
                padding: 20px;
                background: #f0f0f0;
            }
            .box {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 { color: #4CAF50; }
            a {
                display: inline-block;
                margin-top: 20px;
                color: #2196F3;
                text-decoration: none;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="box">
            <h1>✅ Flask is Working!</h1>
            <p>If you see this page, your web server is running correctly.</p>
            <p><strong>Environment:</strong> Production (Render)</p>
            <p><strong>Status:</strong> All systems operational</p>
            <a href="/">← Go to Home Page</a>
        </div>
    </body>
    </html>
    """

@app.route('/health')
def health():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'service': 'flight-price-tracker',
        'tracker_enabled': tracker is not None
    }), 200

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    # Get port from environment variable (Render sets this automatically)
    port = int(os.environ.get('PORT', 5000))
    
    print("\n" + "="*70)
    print("🚀 Flight Price Tracker Web Interface Starting...")
    print("="*70)
    print(f"📱 Server running on port: {port}")
    print("🛑 Press Ctrl+C to stop the server")
    print("="*70 + "\n")
    
    # Run the app
    # host='0.0.0.0' allows external connections (required for Render)
    # debug=False for production (Render will set this)
    app.run(debug=False, host='0.0.0.0', port=port)