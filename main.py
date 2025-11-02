"""
StockWatch Monitor - Replit Entry Point
This file runs the monitor on Replit with proper configuration
"""

import os
import sys

# Replit-specific: Ensure stdout is unbuffered for real-time logs
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(line_buffering=True)  # type: ignore

# Import the monitor and web dashboard
from stockwatch_monitor import monitor_loop
from web_dashboard import start_dashboard

if __name__ == "__main__":
    print("=" * 80)
    print("STOCKWATCH MONITOR - REPLIT MODE")
    print("=" * 80)
    print()
    print("This monitor will run continuously on Replit")
    print("Make sure to set these Secrets in Replit:")
    print("  - TELEGRAM_BOT_TOKEN")
    print("  - TELEGRAM_CHAT_ID")
    print()

    # Start the web dashboard on port 5000
    print("Starting web dashboard on port 5000...")
    try:
        start_dashboard()
        print("✓ Web dashboard started")
        
        # Get the public URL
        domains = os.getenv('REPLIT_DOMAINS', '')
        if domains:
            public_url = f"https://{domains.split(',')[0]}"
        else:
            repl_slug = os.getenv('REPL_SLUG', 'workspace')
            repl_owner = os.getenv('REPL_OWNER', 'user')
            public_url = f"https://{repl_slug}-{repl_owner}.replit.app"
        
        print(f"  Dashboard: {public_url}")
        print(f"  Health Check: {public_url}/health")
        print()
    except Exception as e:
        print(f"⚠ Web dashboard failed to start: {e}")
        print("⚠ Monitor will continue without web interface")
        print()

    print("Starting monitor...")
    print("=" * 80)
    print()

    # Start the monitoring loop
    monitor_loop()
