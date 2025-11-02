# StockWatch Monitor

## Overview

StockWatch Monitor is an automated monitoring system that tracks real-time company announcements from StockWatch.live and delivers instant Telegram notifications. The application scrapes the StockWatch dashboard at regular intervals, identifies new updates, and notifies users via Telegram, while maintaining a persistent record of seen updates to prevent duplicates.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Application Architecture

**Monitoring System Pattern**: The application implements a continuous polling architecture rather than webhook-based notifications. This design choice was made because:
- StockWatch.live doesn't provide an API or webhook system
- Polling at 5-minute intervals provides timely updates without overloading the source
- Simple to deploy and maintain on free hosting platforms

**Entry Point Design**: Two execution modes are supported through separate entry points:
- `main.py` - Replit-optimized entry point with unbuffered output for real-time logging
- `stockwatch_monitor.py` - Standalone script that can run locally with command-line testing

This dual-entry approach allows the same codebase to work seamlessly both on Replit's platform and local development environments.

### Data Persistence

**File-Based State Management**: The application uses JSON file storage (`seen_updates.json`) to track processed updates. This lightweight approach was chosen because:
- No database infrastructure needed - reduces deployment complexity
- Perfect for the data volume (storing UUIDs only)
- Works reliably on Replit's filesystem
- Easy to inspect and debug manually

**Duplicate Prevention**: Each update is identified by a unique UUID extracted from the source website. The system maintains a set of seen IDs in memory and persists to disk, preventing duplicate notifications while surviving restarts.

### Web Scraping

**BeautifulSoup Parsing**: The application uses BeautifulSoup4 for HTML parsing rather than API calls because:
- StockWatch.live doesn't provide a public API
- BeautifulSoup handles inconsistent HTML structures gracefully
- Allows extraction of structured data from semi-structured web pages

**Request Headers**: Custom user-agent headers are used to mimic browser behavior and ensure successful scraping without being blocked.

### Notification System

**Telegram Bot Integration**: Telegram was selected as the notification platform because:
- Free, unlimited notifications
- Cross-platform (mobile, desktop, web)
- Reliable delivery infrastructure
- Simple HTTP API for integration
- Supports rich formatting for update details

**Message Formatting**: Updates are formatted with company name, category, and timestamp to provide actionable information at a glance.

### Deployment Architecture

**Replit Platform Optimizations**: 
- Unbuffered stdout output configured for real-time log visibility in Replit console
- Environment variable-based configuration (Secrets) for sensitive credentials
- Optional Flask keep-alive server (`keep_alive.py`) to maintain Replit instance active

**Console-First Design**: The monitor runs as a console application rather than requiring a web server, reducing resource usage and complexity. The Flask component is optional and used only for Replit's always-on feature.

### Error Handling

**Graceful Degradation**: The application continues running even if individual scrapes fail, implementing retry logic through the continuous loop rather than crashing on errors. This ensures 24/7 monitoring reliability.

**Startup Validation**: The system can run in test mode (`--test` flag) to validate scraping functionality before starting continuous monitoring.

## External Dependencies

### Third-Party Services

**StockWatch.live**: The primary data source, accessed via HTTP requests and HTML parsing. No authentication required. The dashboard URL (`https://www.stockwatch.live/dashboard`) is scraped for live company announcements.

**Telegram Bot API**: Used for push notifications. Requires:
- Bot token (obtained from @BotFather)
- Chat ID (user's Telegram chat identifier)
- Both provided via environment variables

### Python Libraries

**requests (2.31.0)**: HTTP client for fetching StockWatch dashboard and sending Telegram messages.

**beautifulsoup4 (4.12.2)**: HTML parsing library for extracting structured data from StockWatch pages.

**flask (3.0.0)**: Lightweight web framework used optionally for Replit keep-alive server. Not required for core monitoring functionality.

### Platform Services

**Replit**: Target deployment platform providing:
- Free Python hosting environment
- Secrets management for credentials
- Always-on capability (optional)
- Automatic restarts on failure

The application is designed to run standalone without Replit but includes optimizations for that platform.

### Configuration Dependencies

**Environment Variables**:
- `TELEGRAM_BOT_TOKEN`: Authentication token for Telegram bot
- `TELEGRAM_CHAT_ID`: Target chat for notifications

Both can be set via OS environment variables or Replit Secrets.