# Telegram Bot for Daha Courses

This bot allows users to select subjects and difficulty levels to receive notifications about new courses.

## Features

- 🤖 Interactive Telegram bot with inline keyboards
- 📊 User preference management (subjects & difficulties)
- 🔔 Automatic course notifications via webhook
- 💾 SQLite database for user preferences
- 🌐 REST API endpoints for monitoring and integration
- 🔒 Secure webhook processing
- 📈 Statistics and health monitoring

## Quick Start

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create `.env` file:**
   ```
   BOT_TOKEN=your_telegram_bot_token_here
   BOT_DB_URL=postgresql://daha_user:SWP2025@localhost/daha_db
   ```

3. **Run the bot:**
   ```bash
   python main.py
   ```

### Production Deployment

1. **Use the deployment script:**
   ```bash
   sudo ./deploy.sh
   ```

2. **Configure the service:**
   ```bash
   sudo nano /etc/systemd/system/daha-bot.service
   # Set your BOT_TOKEN and BOT_DB_URL
   ```

3. **Start the service:**
   ```bash
   sudo systemctl enable daha-bot
   sudo systemctl start daha-bot
   ```

## API Endpoints

### Webhook
- `POST /webhook/` - Receive new course notifications

### API Endpoints
- `GET /api/` - API information and available endpoints
- `GET /api/health` - Health check for monitoring
- `GET /api/stats` - Bot statistics (users, subjects, difficulties, courses)
- `GET /api/subjects` - Get all available subjects
- `GET /api/difficulties` - Get all available difficulties
- `GET /api/courses` - Get all available courses
- `GET /api/user/{telegram_id}/preferences` - Get user preferences

### Bot Commands
- `/start` - Main menu with subject/difficulty selection

## Architecture

- **Framework**: FastAPI + aiogram
- **Database**: SQLite (user preferences) + PostgreSQL (course data)
- **Port**: 8000 (default)
- **Language**: Russian interface

## Monitoring

- Health check: `GET /api/health`
- Statistics: `GET /api/stats`
- Logs: `sudo journalctl -u daha-bot -f`

## Development

- **Testing**: `python test_bot.py`
- **Linting**: `ruff check .`
- **Formatting**: `ruff format .`

## Files Structure

```
bot/
├── main.py              # Entry point
├── requirements.txt     # Dependencies
├── README.md           # This file
├── test_bot.py         # Test script
├── deploy.sh           # Deployment script
├── daha-bot.service    # Systemd service
└── app/
    ├── main.py         # FastAPI app
    ├── bot.py          # Bot instance
    ├── handlers.py     # Telegram handlers
    ├── models.py       # Database models
    ├── daha_api.py     # API integration
    ├── webhook.py      # Webhook endpoint
    └── api.py          # REST API endpoints
``` 