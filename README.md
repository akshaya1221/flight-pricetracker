# ✈️ Flight Price Tracker & Alert System

A smart notification system that tracks flight prices and alerts users when prices drop, helping travelers save money on bookings.

## 🚀 Features

- 📊 **Real-time Price Tracking** - Monitor flight prices from multiple sources
- 📧 **Email Alerts** - Get notified when prices drop
- 💾 **Price History** - Track price trends over time
- 🎯 **Target Pricing** - Set your budget and get alerted
- 🤖 **Automated Monitoring** - Check prices every 6 hours automatically
- 💻 **CLI Interface** - Easy command-line management

## 📋 Prerequisites

- Python 3.8 or higher
- VS Code (recommended)
- Gmail account (for email alerts)
- Amadeus API account (free tier available)

## 🛠️ Installation

### 1. Clone or Create Project
```bash
mkdir flight-price-tracker
cd flight-price-tracker
```

### 2. Set Up Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
1. Copy `.env.example` to `.env`
2. Fill in your API keys and email credentials

```bash
cp .env.example .env
```

## 🔑 Getting API Keys

### Amadeus API (Flight Data)
1. Go to [Amadeus for Developers](https://developers.amadeus.com)
2. Sign up for free account
3. Create a new app
4. Copy API Key and Secret to `.env`
5. Free tier: 2000 calls/month

### Gmail App Password (Email Alerts)
1. Enable 2-Factor Authentication on your Google account
2. Go to Google Account → Security → 2-Step Verification
3. Scroll to "App Passwords"
4. Generate new app password for "Mail"
5. Copy password to `.env`

## 📖 Usage

### Add a Flight to Track

```bash
# One-way flight
python flight_cli.py add --origin DEL --destination BOM --departure 2025-02-15 --email your@email.com

# Round-trip with target price
python flight_cli.py add --origin DEL --destination BOM --departure 2025-02-15 --return 2025-02-20 --email your@email.com --target 5000
```

### List All Tracked Flights

```bash
python flight_cli.py list
```

### View Price History

```bash
python flight_cli.py history --id 1
```

### Manual Price Check

```bash
python flight_cli.py check
```

### Delete Tracked Flight

```bash
python flight_cli.py delete --id 1
```

### Start Automated Monitoring

```bash
python flight_scheduler.py
```

This will check prices every 6 hours automatically.

## 🗂️ Project Structure

```
flight-price-tracker/
├── flight_tracker.py      # Main tracker with database
├── flight_scraper.py      # Web scraping (Selenium)
├── flight_scheduler.py    # Automated price checks
├── flight_cli.py         # Command-line interface
├── flight_prices.db      # SQLite database (auto-created)
├── .env                  # Your configuration
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 💡 How It Works

1. **Add Flights**: Specify origin, destination, dates, and email
2. **Price Monitoring**: System checks prices via Amadeus API
3. **Database Storage**: All prices stored in SQLite for history
4. **Alert Logic**: Detects 5%+ drops or prices below target
5. **Email Notifications**: Sends formatted alerts to your email
6. **Automation**: Scheduler runs checks every 6 hours

## 🎯 Airport Codes

Common Indian airport codes:
- DEL - Delhi
- BOM - Mumbai
- BLR - Bangalore
- HYD - Hyderabad
- MAA - Chennai
- CCU - Kolkata
- GOI - Goa
- PNQ - Pune

International examples:
- DXB - Dubai
- SIN - Singapore
- LHR - London
- JFK - New York

## ⚙️ Configuration Options

Edit `flight_scheduler.py` to change check frequency:

```python
# Check every 6 hours
schedule.every(6).hours.do(self.check_prices)

# Check daily at specific times
schedule.every().day.at("09:00").do(self.check_prices)
schedule.every().day.at("18:00").do(self.check_prices)

# Check every 12 hours
schedule.every(12).hours.do(self.check_prices)
```

## 🐛 Troubleshooting

### "No module named 'dotenv'"
```bash
pip install python-dotenv
```

### "Invalid API credentials"
- Check your `.env` file has correct API keys
- Verify keys are from Amadeus test environment
- No quotes around values in `.env`

### "SMTP authentication failed"
- Use Gmail App Password, not regular password
- Enable 2FA on Google account first
- Check SMTP settings in `.env`

### ChromeDriver issues (for scraper)
```bash
pip install webdriver-manager
```

## 🚀 Future Enhancements

- [ ] SMS alerts via Twilio
- [ ] Web dashboard with Flask
- [ ] Mobile app notifications
- [ ] ML-based price prediction
- [ ] Multi-airline comparison
- [ ] Telegram bot integration
- [ ] Price drop percentage customization

## 📝 License

MIT License - Feel free to use and modify!

## 🤝 Contributing

Contributions welcome! Feel free to submit issues and pull requests.

## 📧 Support

For issues or questions, please create an issue on GitHub or contact via email.

---

**Happy Travel! ✈️ Save Money! 💰**