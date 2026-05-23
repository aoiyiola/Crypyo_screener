import os
from dotenv import load_dotenv

# Load environment variables from a .env file (if present)
load_dotenv()

# Sensitive configuration — set these in your environment or in a .env file
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

# Strategy configuration
SHORT_MA = 11
LONG_MA = 23
TIMEFRAME = '1h'  # Options: 1h, 4h, 1d
INTERVAL_HOURS = 2  # Sleep time between scans
