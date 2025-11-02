# Quick Start Guide

Get the StockWatch Monitor running in 5 minutes!

## Step 1: Install Dependencies (1 minute)

Open Command Prompt in this folder and run:

```cmd
pip install -r requirements.txt
```

## Step 2: Test the Scraper (30 seconds)

```cmd
python stockwatch_monitor.py --test
```

You should see a list of latest updates from StockWatch. If this works, the monitor is ready!

## Step 3: Run Without Telegram (Optional)

You can start monitoring immediately without Telegram:

```cmd
python stockwatch_monitor.py
```

The monitor will run and display new updates in the console. Press Ctrl+C to stop.

## Step 4: Set Up Telegram (2 minutes)

For push notifications on your phone:

### A. Create Bot
1. Open Telegram, search for `@BotFather`
2. Send: `/newbot`
3. Follow instructions, get your bot token

### B. Get Chat ID
1. Start your bot (click START in Telegram)
2. Run this script:
   ```cmd
   set TELEGRAM_BOT_TOKEN=YOUR_TOKEN_HERE
   python get_chat_id.py
   ```
3. Copy your Chat ID

### C. Set Environment Variables
```cmd
set TELEGRAM_BOT_TOKEN=your_token_here
set TELEGRAM_CHAT_ID=your_chat_id_here
```

**Note**: These are temporary. For permanent setup, see [SETUP_TELEGRAM.md](SETUP_TELEGRAM.md)

### D. Test Telegram
```cmd
python test_telegram.py
```

## Step 5: Start Monitoring!

```cmd
run_monitor.bat
```

OR

```cmd
python stockwatch_monitor.py
```

## What Happens Now?

- Monitor checks StockWatch every 5 minutes
- New company announcements trigger notifications
- Telegram messages sent to your phone
- Console shows all activity
- Press Ctrl+C to stop

## Example Notification

```
🔔 StockWatch Update

Company: GHCL LTD.
Time: 3h ago | 06:31 PM 01-11-2025

News:
GHCL Ltd Announces Q2/H1 FY26 Results,
Unveils Rs. 300 Crore Share Buyback Program

[Read More]
```

## Troubleshooting

### No updates found?
- Check internet connection
- Run: `python scrape_live_updates.py`

### Telegram not working?
- Verify bot token and chat ID
- Run: `python test_telegram.py`
- See: [SETUP_TELEGRAM.md](SETUP_TELEGRAM.md)

### Python not found?
- Install Python 3.7+: https://www.python.org/
- Check "Add to PATH" during installation
- Restart Command Prompt

## Files You Need

Essential:
- `stockwatch_monitor.py` - Main script
- `requirements.txt` - Dependencies

For Telegram:
- `test_telegram.py` - Test notifications
- `get_chat_id.py` - Get your chat ID
- `SETUP_TELEGRAM.md` - Full instructions

Optional:
- `run_monitor.bat` - Easy launcher
- `setup.bat` - Setup wizard

## Next Steps

1. **Run 24/7**: Add to Windows startup (see [README.md](README.md))
2. **Customize**: Change check interval in `stockwatch_monitor.py`
3. **Monitor**: Check `seen_updates.json` for tracked updates

## Need More Help?

- Full documentation: [README.md](README.md)
- Telegram setup: [SETUP_TELEGRAM.md](SETUP_TELEGRAM.md)
- Test each component individually

---

**You're all set! Happy monitoring! 📈**
