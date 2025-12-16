import asyncio
import aiohttp
import os
import logging
from datetime import datetime
from aiogram import Bot

# ================== CONFIG ==================
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = os.getenv("CHANNEL")  # @air_alert_ua_online
ALERTS_URL = "https://alerts.in.ua/alerts.json"
CHECK_INTERVAL = 15  # seconds
# ============================================

# LOGGING
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

bot = Bot(BOT_TOKEN)
active_regions = set()

# DAILY STATS
stats = {
    "alerts": 0,
    "uav": 0,
    "missiles": 0,
    "aviation": 0
}

# ==================
