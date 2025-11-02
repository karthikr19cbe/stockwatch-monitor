"""
StockWatch Monitor - Replit Entry Point
This file runs the monitor on Replit with proper configuration
"""

import os
import sys

# Replit-specific: Ensure stdout is unbuffered for real-time logs
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(line_buffering=True)  # type: ignore

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

    # Keep-alive web server disabled to avoid port conflicts
    # The monitor runs continuously without needing a web server
    print("Note: Monitor runs in console mode (no web server needed)")
    print()

    print("Starting monitor...")
    print("=" * 80)
    print()

    # Start the monitoring loop
    monitor_loop()
