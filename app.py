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