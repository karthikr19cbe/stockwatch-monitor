"""
Keep Alive Web Server for Replit
Runs a simple Flask server to keep the Replit always-on
"""

from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return """
    <html>
    <head>
        <title>StockWatch Monitor</title>
        <meta http-equiv="refresh" content="30">
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background: #1a1a1a;
                color: #00ff00;
            }
            h1 { color: #00ff00; }
            .status {
                background: #2a2a2a;
                padding: 15px;
                border-radius: 5px;
                border: 1px solid #00ff00;
            }
            .running { color: #00ff00; font-weight: bold; }
        </style>
    </head>
    <body>
        <h1>📈 StockWatch Monitor</h1>
        <div class="status">
            <p><span class="running">● RUNNING</span></p>
            <p>Monitoring: <strong>https://www.stockwatch.live/dashboard</strong></p>
            <p>Check interval: <strong>5 minutes</strong></p>
            <p>Status: <strong>Active</strong></p>
        </div>
        <p><small>This page auto-refreshes every 30 seconds</small></p>
    </body>
    </html>
    """

@app.route('/health')
def health():
    return {'status': 'running', 'service': 'stockwatch-monitor'}, 200

def run():
    """Run the Flask server"""
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    """Start the web server in a separate thread"""
    t = Thread(target=run)
    t.daemon = True
    t.start()
