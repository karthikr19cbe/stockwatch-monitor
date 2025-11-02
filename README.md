# StockWatch Live Monitor

🚀 Automated monitoring system for [StockWatch.live](https://www.stockwatch.live/dashboard) live updates with Telegram notifications.

## 🎯 Features

- ✅ Real-time monitoring of company announcements
- ✅ Telegram notifications for new updates
- ✅ Automatic duplicate prevention
- ✅ Runs 24/7 on Replit
- ✅ Easy deployment

## 🚀 Quick Deploy to Replit

[![Run on Replit](https://replit.com/badge/github/your-username/stockwatch-monitor)](https://replit.com/@your-username/stockwatch-monitor)

### 1. Import to Replit

1. Fork this repository or click "Run on Replit" above
2. Replit will automatically import the project

### 2. Configure Secrets

In Replit, click 🔒 **Secrets** and add:

```
TELEGRAM_BOT_TOKEN = your_bot_token_here
TELEGRAM_CHAT_ID = your_chat_id_here
```

### 3. Run

Click the **Run** button. That's it! 🎉

## 📋 What You'll Monitor

- Board meeting intimations
- Financial results
- Acquisitions & investments
- Corporate actions
- BSE/NSE filings
- Management changes
- Contracts & partnerships

## 🔧 Setup Telegram Bot

1. Open Telegram, search **@BotFather**
2. Send `/newbot` and follow instructions
3. Save the bot token
4. Send a message to your bot
5. Get chat ID: Visit `https://api.telegram.org/botYOUR_TOKEN/getUpdates`

Full guide: See [SETUP_TELEGRAM.md](SETUP_TELEGRAM.md)

## 📱 Notification Format

```
Salzer Electronics Reports 22% YoY Revenue Growth...

Read More →
```

Clean, simple, and informative!

## ⚙️ Configuration

Edit `stockwatch_monitor.py`:

```python
CHECK_INTERVAL = 300  # Check every 5 minutes
```

## 🔒 Security

- ✅ Credentials stored in Replit Secrets
- ✅ `.gitignore` prevents sensitive data commits
- ✅ No database - file-based tracking

## 📊 Requirements

- Python 3.11+
- Replit account (free)
- Telegram bot

## 🤝 Contributing

Feel free to fork and improve!

## 📄 License

Free for personal use

## 🙏 Acknowledgments

Inspired by nuvama-news-monitor architecture

---

**Built for tracking Indian stock market updates** 📈
