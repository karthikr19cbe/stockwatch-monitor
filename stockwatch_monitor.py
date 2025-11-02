"""
StockWatch Live Updates Monitor
Monitors https://www.stockwatch.live/dashboard for new company announcements
and sends Telegram notifications for new updates.
"""

import sys
import io
import requests
from bs4 import BeautifulSoup
import json
import time
import re
from datetime import datetime
from urllib.parse import unquote
import os

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Configuration
STOCKWATCH_URL = "https://www.stockwatch.live/dashboard"
SEEN_UPDATES_FILE = "seen_updates.json"
CHECK_INTERVAL = 300  # Check every 5 minutes (300 seconds)
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')

def load_seen_updates():
    """Load previously seen update IDs from file"""
    try:
        if os.path.exists(SEEN_UPDATES_FILE):
            with open(SEEN_UPDATES_FILE, 'r', encoding='utf-8') as f:
                return set(json.load(f))
        return set()
    except Exception as e:
        print(f"[WARNING] Could not load seen updates: {e}")
        return set()

def save_seen_updates(seen_ids):
    """Save seen update IDs to file"""
    try:
        with open(SEEN_UPDATES_FILE, 'w', encoding='utf-8') as f:
            json.dump(list(seen_ids), f, indent=2)
    except Exception as e:
        print(f"[ERROR] Could not save seen updates: {e}")

def scrape_live_updates():
    """Scrape live updates from StockWatch dashboard"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }

        response = requests.get(STOCKWATCH_URL, headers=headers, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        updates = []

        # Find all news links with newsId parameter
        all_links = soup.find_all('a', href=True)
        news_items = [link for link in all_links if 'newsId=' in str(link.get('href', ''))]

        for item in news_items:
            try:
                href = item.get('href', '')

                # Extract newsId
                news_id_match = re.search(r'newsId=([^&]+)', href)
                news_id = news_id_match.group(1) if news_id_match else None

                if not news_id:
                    continue

                # Extract company name
                name_match = re.search(r'name=([^&]+)', href)
                company = unquote(name_match.group(1)) if name_match else 'Unknown Company'

                # Extract title
                title_match = re.search(r'title=([^&]+)', href)
                title = unquote(title_match.group(1)) if title_match else None

                # Find title from page if not in URL
                if not title:
                    title_elem = item.find('h2')
                    if not title_elem:
                        title_elem = item.find('h3')
                    title = title_elem.get_text(strip=True) if title_elem else 'No title available'

                # Find timestamp
                timestamp_elem = item.find('h6', style=lambda x: x and 'color' in str(x))
                timestamp = timestamp_elem.get_text(strip=True) if timestamp_elem else 'Just now'

                # Build full URL
                full_url = f"https://www.stockwatch.live/{href}" if not href.startswith('http') else href

                update = {
                    'id': news_id,
                    'company': company,
                    'title': title,
                    'timestamp': timestamp,
                    'url': full_url,
                    'scraped_at': datetime.now().isoformat()
                }

                updates.append(update)

            except Exception as e:
                print(f"[WARNING] Failed to parse news item: {e}")
                continue

        return updates

    except Exception as e:
        print(f"[ERROR] Failed to scrape updates: {e}")
        return []

def send_telegram_message(message):
    """Send message via Telegram bot"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("[INFO] Telegram not configured. Skipping notification.")
        return False

    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': message,
            'parse_mode': 'HTML',
            'disable_web_page_preview': False
        }

        response = requests.post(url, data=data, timeout=10)
        response.raise_for_status()
        return True

    except Exception as e:
        print(f"[ERROR] Failed to send Telegram message: {e}")
        return False

def format_update_message(update):
    """Format update as Telegram message"""
    message = f"""{update['title']}

<a href="{update['url']}">Read More</a>
"""
    return message

def monitor_loop():
    """Main monitoring loop"""
    print("=" * 80)
    print("STOCKWATCH LIVE UPDATES MONITOR")
    print("=" * 80)
    print(f"Target URL: {STOCKWATCH_URL}")
    print(f"Check Interval: {CHECK_INTERVAL} seconds ({CHECK_INTERVAL//60} minutes)")
    print(f"Telegram Enabled: {'Yes' if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID else 'No'}")
    print("=" * 80)
    print()

    seen_ids = load_seen_updates()
    print(f"[INFO] Loaded {len(seen_ids)} previously seen updates")

    iteration = 0

    while True:
        iteration += 1
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"\n[{current_time}] Check #{iteration}")
        print("-" * 80)

        # Scrape updates
        updates = scrape_live_updates()

        if not updates:
            print("[WARNING] No updates found or scraping failed")
        else:
            print(f"[INFO] Found {len(updates)} total updates on page")

            # Check for new updates
            new_updates = [u for u in updates if u['id'] not in seen_ids]

            if new_updates:
                print(f"[NEW] Found {len(new_updates)} new update(s)!")
                print()

                # Reverse order so oldest messages are sent first (latest appears last in Telegram)
                new_updates.reverse()

                for idx, update in enumerate(new_updates, 1):
                    print(f"  [{idx}] {update['company']}")
                    print(f"      {update['title'][:80]}...")
                    print(f"      Time: {update['timestamp']}")
                    print()

                    # Send Telegram notification
                    message = format_update_message(update)
                    if send_telegram_message(message):
                        print(f"      ✓ Telegram notification sent")
                    else:
                        print(f"      ⚠ Telegram notification skipped")

                    # Mark as seen
                    seen_ids.add(update['id'])

                    # Small delay between notifications
                    time.sleep(1)

                # Save updated seen list
                save_seen_updates(seen_ids)
                print(f"\n[INFO] Saved {len(seen_ids)} seen updates to file")

            else:
                print("[INFO] No new updates found")

        print(f"\n[INFO] Waiting {CHECK_INTERVAL} seconds until next check...")
        print(f"[INFO] Next check at: {datetime.fromtimestamp(time.time() + CHECK_INTERVAL).strftime('%H:%M:%S')}")

        # Wait before next check
        time.sleep(CHECK_INTERVAL)

def test_single_check():
    """Run a single check (for testing)"""
    print("=" * 80)
    print("STOCKWATCH MONITOR - TEST MODE")
    print("=" * 80)
    print()

    print("[INFO] Running single check...")
    updates = scrape_live_updates()

    if updates:
        print(f"\n[SUCCESS] Found {len(updates)} updates")
        print("\n" + "=" * 80)
        print("LATEST UPDATES:")
        print("=" * 80)

        for idx, update in enumerate(updates[:5], 1):
            print(f"\n[{idx}] {update['timestamp']}")
            print(f"    Company: {update['company']}")
            print(f"    Title: {update['title'][:80]}...")
            print(f"    URL: {update['url']}")

        if len(updates) > 5:
            print(f"\n... and {len(updates) - 5} more updates")

    else:
        print("[ERROR] No updates found")

    print("\n" + "=" * 80)
    print("Test completed!")
    print("=" * 80)

if __name__ == "__main__":
    # Check if running in test mode
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        test_single_check()
    else:
        try:
            monitor_loop()
        except KeyboardInterrupt:
            print("\n\n[INFO] Monitor stopped by user")
            print("=" * 80)
