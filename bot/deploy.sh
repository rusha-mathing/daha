#!/bin/bash

# Daha Bot Deployment Script
# This script sets up the bot on a Ubuntu VPS

set -e

echo "🚀 Starting Daha Bot deployment..."

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Please run as root (use sudo)"
    exit 1
fi

# Create daha user if it doesn't exist
if ! id "daha" &>/dev/null; then
    echo "👤 Creating daha user..."
    useradd -m -s /bin/bash daha
    usermod -aG sudo daha
fi

# Create application directory
echo "📁 Setting up application directory..."
mkdir -p /opt/daha/bot
chown daha:daha /opt/daha/bot

# Copy bot files
echo "📋 Copying bot files..."
cp -r . /opt/daha/bot/
chown -R daha:daha /opt/daha/bot

# Set up Python virtual environment
echo "🐍 Setting up Python environment..."
cd /opt/daha/bot
sudo -u daha python3 -m venv venv
sudo -u daha venv/bin/pip install --upgrade pip
sudo -u daha venv/bin/pip install -r requirements.txt

# Set up systemd service
echo "⚙️ Setting up systemd service..."
cp daha-bot.service /etc/systemd/system/
systemctl daemon-reload

# Create log directory
echo "📝 Setting up logging..."
mkdir -p /var/log/daha-bot
chown daha:daha /var/log/daha-bot

echo "✅ Bot deployment completed!"
echo ""
echo "📋 Next steps:"
echo "1. Edit /etc/systemd/system/daha-bot.service"
echo "2. Set your BOT_TOKEN and BOT_DB_URL"
echo "3. Enable and start the service:"
echo "   sudo systemctl enable daha-bot"
echo "   sudo systemctl start daha-bot"
echo "4. Check status: sudo systemctl status daha-bot"
echo "5. View logs: sudo journalctl -u daha-bot -f" 