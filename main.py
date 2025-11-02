"""
StockWatch Monitor - Replit Entry Point
This file runs the monitor on Replit with proper configuration
"""

import os
import sys

# Replit-specific: Ensure stdout is unbuffered for real-time logs
sys.stdout.reconfigure(line_buffering=True)

# Import keep_alive to run web server (keeps Replit alive)
from keep_alive import keep_alive

# Import the monitor
from stockwatch_monitor import monitor_loop

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

    # Start keep-alive web server
    print("Starting keep-alive web server on port 8080...")
    keep_alive()
    print("✓ Web server started")
    print()

    print("Starting monitor...")
    print("=" * 80)
    print()

    # Start the monitoring loop
    monitor_loop()
