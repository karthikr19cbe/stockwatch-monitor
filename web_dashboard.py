"""
StockWatch Monitor - Web Dashboard
Shows monitor status and recent updates in a web interface
"""

from flask import Flask, render_template_string
import json
import os
from datetime import datetime
from threading import Thread
import time

app = Flask(__name__)

# Global variables to track monitor status
monitor_status = {
    'running': True,
    'last_check': None,
    'total_updates_seen': 0,
    'telegram_enabled': False,
    'next_check': None
}

def load_seen_updates_count():
    """Load count of seen updates"""
    try:
        if os.path.exists('seen_updates.json'):
            with open('seen_updates.json', 'r') as f:
                data = json.load(f)
                return len(data)
        return 0
    except:
        return 0

def update_status():
    """Update status information"""
    monitor_status['total_updates_seen'] = load_seen_updates_count()
    monitor_status['last_check'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    monitor_status['telegram_enabled'] = bool(os.getenv('TELEGRAM_BOT_TOKEN') and os.getenv('TELEGRAM_CHAT_ID'))

# HTML Template for the dashboard
DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>StockWatch Monitor Dashboard</title>
    <meta http-equiv="refresh" content="30">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: #ffffff;
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            padding: 40px 20px;
            margin-bottom: 30px;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header .subtitle {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .status-cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 25px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }
        
        .card h3 {
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
            opacity: 0.8;
            margin-bottom: 10px;
        }
        
        .card .value {
            font-size: 2em;
            font-weight: bold;
            margin-top: 10px;
        }
        
        .status-indicator {
            display: inline-flex;
            align-items: center;
            gap: 10px;
        }
        
        .status-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #00ff00;
            box-shadow: 0 0 10px #00ff00;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .info-section {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 30px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            margin-bottom: 20px;
        }
        
        .info-section h2 {
            margin-bottom: 20px;
            font-size: 1.8em;
        }
        
        .info-row {
            display: flex;
            justify-content: space-between;
            padding: 15px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .info-row:last-child {
            border-bottom: none;
        }
        
        .info-label {
            opacity: 0.8;
        }
        
        .info-value {
            font-weight: bold;
        }
        
        .enabled {
            color: #00ff88;
        }
        
        .footer {
            text-align: center;
            padding: 20px;
            opacity: 0.6;
            font-size: 0.9em;
        }
        
        .api-endpoint {
            background: rgba(0, 0, 0, 0.3);
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
            font-family: 'Courier New', monospace;
            word-break: break-all;
        }
        
        @media (max-width: 768px) {
            .header h1 {
                font-size: 1.8em;
            }
            
            .status-cards {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📈 StockWatch Monitor</h1>
            <p class="subtitle">Live News Monitoring Dashboard</p>
        </div>
        
        <div class="status-cards">
            <div class="card">
                <h3>Monitor Status</h3>
                <div class="value status-indicator">
                    <span class="status-dot"></span>
                    RUNNING
                </div>
            </div>
            
            <div class="card">
                <h3>Updates Tracked</h3>
                <div class="value">{{ total_updates }}</div>
            </div>
            
            <div class="card">
                <h3>Telegram Alerts</h3>
                <div class="value enabled">{{ 'ENABLED' if telegram_enabled else 'DISABLED' }}</div>
            </div>
            
            <div class="card">
                <h3>Check Interval</h3>
                <div class="value">5 MIN</div>
            </div>
        </div>
        
        <div class="info-section">
            <h2>Monitor Configuration</h2>
            
            <div class="info-row">
                <span class="info-label">Target Website</span>
                <span class="info-value">stockwatch.live/dashboard</span>
            </div>
            
            <div class="info-row">
                <span class="info-label">Last Check</span>
                <span class="info-value">{{ last_check or 'Starting...' }}</span>
            </div>
            
            <div class="info-row">
                <span class="info-label">Auto Refresh</span>
                <span class="info-value">Every 30 seconds</span>
            </div>
        </div>
        
        <div class="info-section">
            <h2>UptimeRobot Health Endpoint</h2>
            <p>Use this URL to monitor your app with UptimeRobot:</p>
            <div class="api-endpoint">
                {{ base_url }}/health
            </div>
            <p style="margin-top: 10px; opacity: 0.8; font-size: 0.9em;">
                This endpoint returns a 200 OK status when the monitor is running.
            </p>
        </div>
        
        <div class="footer">
            <p>Monitoring Indian Stock Market Updates • Powered by Replit</p>
            <p style="margin-top: 5px;">Page auto-refreshes every 30 seconds</p>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def dashboard():
    """Main dashboard page"""
    update_status()
    
    # Get the base URL for the health endpoint
    domains = os.getenv('REPLIT_DOMAINS', '')
    if domains:
        base_domain = f"https://{domains.split(',')[0]}"
    else:
        repl_slug = os.getenv('REPL_SLUG', 'your-repl')
        repl_owner = os.getenv('REPL_OWNER', 'username')
        base_domain = f"https://{repl_slug}-{repl_owner}.replit.app"
    
    return render_template_string(
        DASHBOARD_HTML,
        total_updates=monitor_status['total_updates_seen'],
        last_check=monitor_status['last_check'],
        telegram_enabled=monitor_status['telegram_enabled'],
        next_check=monitor_status.get('next_check'),
        base_url=base_domain
    )

@app.route('/health')
def health():
    """Health check endpoint for UptimeRobot"""
    return {
        'status': 'ok',
        'service': 'stockwatch-monitor',
        'running': True,
        'timestamp': datetime.now().isoformat(),
        'updates_tracked': monitor_status['total_updates_seen']
    }, 200

@app.route('/status')
def status():
    """JSON status endpoint"""
    update_status()
    return {
        'status': 'running',
        'last_check': monitor_status['last_check'],
        'total_updates_seen': monitor_status['total_updates_seen'],
        'telegram_enabled': monitor_status['telegram_enabled']
    }

def run_flask():
    """Run the Flask web server"""
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

def start_dashboard():
    """Start the dashboard in a separate thread"""
    thread = Thread(target=run_flask, daemon=True)
    thread.start()
    return thread

if __name__ == '__main__':
    run_flask()
