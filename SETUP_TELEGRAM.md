# Telegram Bot Setup Guide

This guide will help you set up Telegram notifications for the StockWatch Monitor.

## Step 1: Create a Telegram Bot

1. Open Telegram and search for **@BotFather**
2. Start a chat with BotFather
3. Send the command: `/newbot`
4. Follow the instructions:
   - Choose a name for your bot (e.g., "StockWatch Monitor")
   - Choose a username for your bot (must end in 'bot', e.g., "stockwatch_alerts_bot")
5. BotFather will give you a **Bot Token** - it looks like this:
   ```
   123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   ```
6. **Save this token securely!** You'll need it in the next steps.

## Step 2: Start Your Bot

1. Click the link BotFather provides or search for your bot's username
2. Click **START** or send `/start` to your bot
3. Send any message to your bot (e.g., "Hello")

## Step 3: Get Your Chat ID

### Option A: Using the get_chat_id.py script (Recommended)

1. Open Command Prompt or PowerShell
2. Navigate to the StockWatch Monitor folder
3. Set your bot token temporarily:
   ```cmd
   set TELEGRAM_BOT_TOKEN=your_bot_token_here
   ```
4. Run the script:
   ```cmd
   python get_chat_id.py
   ```
5. The script will display your Chat ID

### Option B: Manual method

1. Send a message to your bot
2. Open this URL in your browser (replace YOUR_BOT_TOKEN):
   ```
   https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates
   ```
3. Look for `"chat":{"id":123456789` - that number is your Chat ID

## Step 4: Configure Environment Variables

### Option A: Windows Environment Variables (Persistent)

1. Press `Win + R` and type `sysdm.cpl`
2. Go to **Advanced** tab → **Environment Variables**
3. Under **User variables**, click **New**
4. Add these two variables:
   - Variable name: `TELEGRAM_BOT_TOKEN`
     Value: Your bot token from Step 1
   - Variable name: `TELEGRAM_CHAT_ID`
     Value: Your chat ID from Step 3
5. Click **OK** to save
6. **Restart your Command Prompt** for changes to take effect

### Option B: Command Prompt (Temporary - for this session only)

```cmd
set TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
set TELEGRAM_CHAT_ID=987654321
```

### Option C: Create a .env file (Advanced)

1. Create a file named `.env` in the StockWatch Monitor folder
2. Add these lines:
   ```
   TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   TELEGRAM_CHAT_ID=987654321
   ```
3. You'll need to install python-dotenv: `pip install python-dotenv`

## Step 5: Test the Configuration

Run the test script to verify everything works:

```cmd
python test_telegram.py
```

If successful, you should receive a test message in Telegram!

## Troubleshooting

### "Bot token is invalid"
- Double-check you copied the entire token from BotFather
- Make sure there are no extra spaces

### "Chat ID not found"
- Make sure you sent a message to your bot first
- Try running get_chat_id.py again

### "No message received in Telegram"
- Check that you've set both TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID
- Verify the values are correct
- Make sure you clicked START on your bot
- Check your internet connection

### Environment variables not working
- Make sure you restarted Command Prompt after setting them
- Try the temporary method (Option B) first to test
- Verify variables are set: `echo %TELEGRAM_BOT_TOKEN%`

## Privacy & Security

- **Never share your bot token publicly!**
- The bot token gives full control over your bot
- If compromised, use BotFather's `/revoke` command to get a new token
- Chat IDs are safe to share (they're just numbers)

## Next Steps

Once Telegram is configured:

1. Run the monitor: `run_monitor.bat`
2. You'll receive notifications for new StockWatch updates!

## Need Help?

- Check Telegram Bot API docs: https://core.telegram.org/bots/api
- Re-run the setup: `setup.bat`
- Test individual components: `test_telegram.py`
