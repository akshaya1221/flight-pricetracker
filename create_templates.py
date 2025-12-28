import os

# Create templates directory if it doesn't exist
os.makedirs('templates', exist_ok=True)

# index.html content
index_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flight Price Tracker</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        .header {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
            text-align: center;
        }
        .header h1 { color: #667eea; font-size: 2.5em; margin-bottom: 10px; }
        .btn {
            display: inline-block;
            padding: 15px 30px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 10px;
            font-weight: bold;
            transition: all 0.3s;
        }
        .btn:hover {
            background: #5568d3;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        .alert {
            padding: 15px 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .alert-success { background: #d1fae5; color: #065f46; }
        .alert-error { background: #fee2e2; color: #991b1b; }
        .flights-container {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .flights-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
        }
        .flight-card {
            background: #f9fafb;
            border: 2px solid #e5e7eb;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .flight-route {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 15px;
            font-size: 1.5em;
            font-weight: bold;
            color: #667eea;
        }
        .btn-check {
            background: #10b981;
            padding: 10px 20px;
            font-size: 0.9em;
            margin-right: 10px;
        }
        .btn-history {
            background: #f59e0b;
            padding: 10px 20px;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>✈️ Flight Price Tracker</h1>
            <p>Monitor flight prices and get instant alerts!</p>
        </div>
        
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        <div class="flights-container">
            <div class="flights-header">
                <h2>📋 Your Tracked Flights ({{ flights|length }})</h2>
                <a href="{{ url_for('add_flight') }}" class="btn">➕ Add New Flight</a>
            </div>
            
            {% if flights %}
                {% for flight in flights %}
                <div class="flight-card">
                    <div class="flight-route">
                        {{ flight[1] }} ✈️ {{ flight[2] }}
                    </div>
                    <p>📅 Date: {{ flight[3] }} | 📧 Email: {{ flight[4] }}</p>
                    {% if flight[5] %}
                        <p>🎯 Target Price: ₹{{ flight[5] }}</p>
                    {% endif %}
                    <div style="margin-top: 15px;">
                        <a href="{{ url_for('check_flight', flight_id=flight[0]) }}" class="btn btn-check">
                            🔍 Check Price
                        </a>
                        <a href="{{ url_for('price_history', flight_id=flight[0]) }}" class="btn btn-history">
                            📈 History
                        </a>
                    </div>
                </div>
                {% endfor %}
            {% else %}
                <div style="text-align: center; padding: 60px;">
                    <h3>No flights tracked yet</h3>
                    <p>Start by adding your first flight!</p>
                    <br>
                    <a href="{{ url_for('add_flight') }}" class="btn">➕ Add Your First Flight</a>
                </div>
            {% endif %}
        </div>
    </div>
</body>
</html>'''

# add_flight.html content
add_flight_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Add Flight</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 800px; margin: 0 auto; }
        .header {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
            text-align: center;
        }
        .header h1 { color: #667eea; font-size: 2em; }
        .form-container {
            background: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .form-group { margin-bottom: 25px; }
        label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 600;
            font-size: 1.05em;
        }
        input {
            width: 100%;
            padding: 15px;
            border: 2px solid #e5e7eb;
            border-radius: 10px;
            font-size: 1em;
        }
        input:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        .btn {
            width: 100%;
            padding: 15px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 10px;
            font-weight: bold;
            font-size: 1em;
            cursor: pointer;
            margin-bottom: 10px;
        }
        .btn:hover {
            background: #5568d3;
            transform: translateY(-2px);
        }
        .btn-secondary {
            background: #6b7280;
            text-align: center;
            display: block;
            text-decoration: none;
        }
        .help-text {
            font-size: 0.9em;
            color: #666;
            margin-top: 5px;
        }
        .airport-codes {
            background: #f9fafb;
            padding: 20px;
            border-radius: 10px;
            margin-top: 30px;
        }
        .codes-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin-top: 15px;
        }
        .code-item {
            background: white;
            padding: 10px;
            border-radius: 8px;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>➕ Add New Flight to Track</h1>
            <p>Enter flight details to start monitoring prices</p>
        </div>
        
        <div class="form-container">
            <form method="POST" action="{{ url_for('add_flight') }}">
                <div class="form-group">
                    <label for="origin">🛫 From (Airport Code)</label>
                    <input type="text" id="origin" name="origin" required 
                           placeholder="e.g., DEL" maxlength="3" style="text-transform: uppercase;">
                    <p class="help-text">3-letter airport code</p>
                </div>
                
                <div class="form-group">
                    <label for="destination">🛬 To (Airport Code)</label>
                    <input type="text" id="destination" name="destination" required 
                           placeholder="e.g., BOM" maxlength="3" style="text-transform: uppercase;">
                    <p class="help-text">3-letter airport code</p>
                </div>
                
                <div class="form-group">
                    <label for="departure_date">📅 Departure Date</label>
                    <input type="date" id="departure_date" name="departure_date" required>
                </div>
                
                <div class="form-group">
                    <label for="email">📧 Email for Alerts</label>
                    <input type="email" id="email" name="email" required 
                           placeholder="your.email@example.com"
                           value="akshaya.morampudi@gmail.com">
                </div>
                
                <div class="form-group">
                    <label for="target_price">🎯 Target Price (Optional)</label>
                    <input type="number" id="target_price" name="target_price" 
                           placeholder="e.g., 5000" step="100" min="0">
                    <p class="help-text">Alert when price drops below this (in ₹)</p>
                </div>
                
                <button type="submit" class="btn">✈️ Start Tracking This Flight</button>
                <a href="{{ url_for('index') }}" class="btn btn-secondary">← Back to Home</a>
            </form>
            
            <div class="airport-codes">
                <h3>📍 Common Airport Codes (India)</h3>
                <div class="codes-grid">
                    <div class="code-item"><strong>DEL</strong> - Delhi</div>
                    <div class="code-item"><strong>BOM</strong> - Mumbai</div>
                    <div class="code-item"><strong>BLR</strong> - Bangalore</div>
                    <div class="code-item"><strong>MAA</strong> - Chennai</div>
                    <div class="code-item"><strong>HYD</strong> - Hyderabad</div>
                    <div class="code-item"><strong>GOI</strong> - Goa</div>
                </div>
            </div>
        </div>
    </div>
    <script>
        const today = new Date().toISOString().split('T')[0];
        document.getElementById('departure_date').setAttribute('min', today);
    </script>
</body>
</html>'''

# history.html content
history_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Price History</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1000px; margin: 0 auto; }
        .header {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
        }
        .header h1 { color: #667eea; font-size: 2em; }
        .history-container {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .btn {
            padding: 12px 24px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 10px;
            font-weight: bold;
            display: inline-block;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            padding: 15px;
            text-align: left;
            border-bottom: 1px solid #e5e7eb;
        }
        th { background: #f9fafb; font-weight: 600; }
        tr:hover { background: #f9fafb; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📈 Price History</h1>
            {% if flight %}
                <p style="margin-top: 10px; font-size: 1.2em;">
                    <strong>{{ flight[1] }} ✈️ {{ flight[2] }}</strong> on {{ flight[3] }}
                </p>
            {% endif %}
        </div>
        
        <div class="history-container">
            <a href="{{ url_for('index') }}" class="btn">← Back to Home</a>
            
            {% if history %}
                <table>
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Price</th>
                            <th>Checked At</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for price, checked_at in history %}
                        <tr>
                            <td>{{ loop.index }}</td>
                            <td><strong>₹{{ price }}</strong></td>
                            <td>{{ checked_at }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            {% else %}
                <div style="text-align: center; padding: 60px;">
                    <h3>No price history available</h3>
                    <p>Check the price to start tracking!</p>
                </div>
            {% endif %}
        </div>
    </div>
</body>
</html>'''

# Write the files
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)
    print("✅ Created templates/index.html")

with open('templates/add_flight.html', 'w', encoding='utf-8') as f:
    f.write(add_flight_html)
    print("✅ Created templates/add_flight.html")

with open('templates/history.html', 'w', encoding='utf-8') as f:
    f.write(history_html)
    print("✅ Created templates/history.html")

print("\n🎉 All HTML templates created successfully!")
print("📝 You can now run: python app.py")