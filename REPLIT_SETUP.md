# Running StockWatch Monitor on Replit

This guide shows you how to deploy the StockWatch Monitor on Replit for 24/7 monitoring.

## Why Replit?

- ✅ Free hosting (with always-on option)
- ✅ Runs 24/7 (unlike your local computer)
- ✅ Easy setup - no server management
- ✅ Works alongside your Nuvama monitor
- ✅ Automatic restarts if it crashes

## Step 1: Create Replit Account

1. Go to [replit.com](https://replit.com)
2. Sign up or log in
3. Click **"+ Create Repl"**

## Step 2: Upload Project

### Option A: Import from GitHub (Recommended)
1. Push your StockWatch Monitor to GitHub
2. In Replit, click **"Import from GitHub"**
3. Paste your repository URL
4. Click **"Import from GitHub"**

### Option B: Manual Upload
1. Create a new Python Repl
2. Upload these files:
   - `main.py`
   - `stockwatch_monitor.py`
   - `keep_alive.py`
   - `requirements.txt`
   - `.replit`
   - `replit.nix`

## Step 3: Configure Secrets (Telegram Credentials)

### About Telegram Bot

**IMPORTANT: You can use the SAME bot for both monitors!**
- ✅ One Telegram bot can send messages to multiple monitors
- ✅ Same `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` for both
- ✅ You'll receive messages from both Nuvama and StockWatch in the same chat

**OR create a separate bot if you prefer:**
- Different bots for organizational purposes
- Separate chats for different types of updates

### Setting Secrets in Replit

1. In your Repl, click the **🔒 Secrets** (lock icon) in the left sidebar
2. Add these two secrets:

   **Secret 1:**
   - Key: `TELEGRAM_BOT_TOKEN`
   - Value: Your Telegram bot token (from @BotFather)

   **Secret 2:**
   - Key: `TELEGRAM_CHAT_ID`
   - Value: Your Telegram chat ID

3. Click **"Add new secret"** for each

### If You Don't Have Telegram Set Up Yet

See `SETUP_TELEGRAM.md` for instructions on:
- Creating a bot with @BotFather
- Getting your bot token
- Finding your chat ID

**Pro Tip:** Use the same credentials from your Nuvama monitor!

## Step 4: Install Dependencies

Replit will automatically install packages from `requirements.txt`, but you can also run manually:

```bash
pip install -r requirements.txt
```

## Step 5: Run the Monitor

Click the big green **"Run"** button at the top!

You should see:
```
================================================================================
STOCKWATCH MONITOR - REPLIT MODE
================================================================================

This monitor will run continuously on Replit
Make sure to set these Secrets in Replit:
  - TELEGRAM_BOT_TOKEN
  - TELEGRAM_CHAT_ID

Starting keep-alive web server on port 8080...
✓ Web server started

Starting monitor...
================================================================================

[2025-11-01 22:30:00] Check #1
--------------------------------------------------------------------------------
Found 34 total updates on page
[INFO] No new updates found
...
```

## Step 6: Keep It Running 24/7

### Option A: Replit Always-On (Paid - $7/month)
1. Go to your Repl settings
2. Enable **"Always On"**
3. Your monitor will run forever without stopping

### Option B: UptimeRobot (Free)
1. Go to [uptimerobot.com](https://uptimerobot.com)
2. Create free account
3. Add new monitor:
   - Type: HTTP(s)
   - URL: Your Repl's web URL (e.g., `https://stockwatch-monitor.yourname.repl.co`)
   - Interval: 5 minutes
4. UptimeRobot will ping your Repl every 5 minutes, keeping it alive

### Getting Your Repl URL
- Click the **"Open in new tab"** button at the top
- Copy the URL (e.g., `https://stockwatch-monitor.yourname.repl.co`)
- Use this URL in UptimeRobot

## Step 7: Verify It's Working

### Check the Console
You should see regular check messages:
```
[2025-11-01 22:30:00] Check #1
Found 34 total updates on page
[INFO] No new updates found
Waiting 300 seconds until next check...
```

### Check Telegram
- You should receive a notification when a new update appears
- Both Nuvama and StockWatch updates will appear in the same chat (if using same bot)

### Check the Web Interface
Open your Repl URL in a browser to see:
```
📈 StockWatch Monitor
● RUNNING
Monitoring: https://www.stockwatch.live/dashboard
Check interval: 5 minutes
Status: Active
```

## Troubleshooting

### "Secrets not found" Error
- Make sure you added both secrets in the Secrets panel
- Names must be EXACT: `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`
- No spaces or typos

### "No module named 'flask'" Error
```bash
pip install flask
```

### Monitor Keeps Stopping
- Free Repls sleep after 1 hour of inactivity
- Use UptimeRobot (free) or Replit Always-On (paid) to keep it running

### Not Receiving Telegram Messages
- Check your bot token and chat ID are correct
- Make sure you've sent `/start` to your bot
- Test with: Create a new file `test.py` and run:
```python
import os
import requests

bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')

url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
requests.post(url, data={'chat_id': chat_id, 'text': 'Test from Replit'})
```

### Repl Runs Out of Memory
- This shouldn't happen with this lightweight monitor
- If it does, restart the Repl

## Managing Both Monitors

You'll have two Repls running:
1. **Nuvama News Monitor** - Your existing one
2. **StockWatch Monitor** - This new one

Both can:
- ✅ Use the same Telegram bot
- ✅ Send to the same chat
- ✅ Run simultaneously
- ✅ Have their own `seen_updates.json` (no conflicts)

**Example Telegram flow:**
```
🔔 Nuvama Update
Company: XYZ Ltd
News: Financial Results...
[From Nuvama Monitor]

🔔 StockWatch Update
Company: ABC Ltd
News: Board Meeting...
[From StockWatch Monitor]
```

## Files Overview

- `main.py` - Replit entry point (runs on start)
- `stockwatch_monitor.py` - Core monitoring logic
- `keep_alive.py` - Web server to keep Repl alive
- `requirements.txt` - Python dependencies
- `.replit` - Replit configuration
- `replit.nix` - Nix environment config
- `seen_updates.json` - Auto-created, tracks seen updates

## Customization

### Change Check Interval

Edit `stockwatch_monitor.py`:
```python
CHECK_INTERVAL = 300  # Seconds (5 minutes)
```

Common values:
- `180` - 3 minutes (more frequent)
- `300` - 5 minutes (default)
- `600` - 10 minutes (less frequent)

### Different Telegram Bot

If you want separate bots for Nuvama and StockWatch:

1. Create a new bot with @BotFather
2. Get new bot token
3. Use same chat ID (or different one for separate chats)
4. Set in Replit Secrets

## Monitoring Performance

### View Logs
- Click **"Console"** tab in Replit to see real-time logs
- Shows all checks, new updates, and errors

### Check Uptime
- UptimeRobot dashboard shows uptime percentage
- Should be 99%+ with proper setup

### Storage
- `seen_updates.json` grows slowly (~100 bytes per update)
- After 1 year: ~3MB (not an issue)
- Replit has plenty of storage

## Cost Summary

### Free Option
- ✅ Replit: Free tier
- ✅ UptimeRobot: Free tier (50 monitors)
- ✅ Telegram: Free
- **Total: $0/month**

Limitations:
- Repl sleeps after 1 hour (UptimeRobot keeps it awake)
- May have occasional downtime

### Paid Option (Recommended for 24/7)
- Replit Always-On: $7/month
- **Total: $7/month**

Benefits:
- True 24/7 uptime
- No sleep
- Faster response times

## Next Steps

1. ✅ Upload project to Replit
2. ✅ Set Telegram secrets
3. ✅ Click Run
4. ✅ Set up UptimeRobot (optional but recommended)
5. ✅ Monitor is running!

## Support

- Replit Docs: [docs.replit.com](https://docs.replit.com)
- Replit Community: [replit.com/talk](https://replit.com/talk)
- This monitor's docs: See `README.md`

---

**You're all set to run StockWatch Monitor 24/7 on Replit!** 🚀
