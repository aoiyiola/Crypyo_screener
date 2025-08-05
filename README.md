# 🧠 Crypto Screener with MA Crossover + Telegram Alerts 📈

This Python-based screener scans the **Top 100 Binance crypto pairs** every 2 hours, applies a **Moving Average crossover strategy**, and sends a **Telegram alert with candlestick chart** if a bullish or bearish signal is detected.

---

## 📦 Features

- ✅ Real-time Top 100 Binance pairs (sorted by 24h volume)
- 📊 MA crossover strategy (customizable)
- 📉 Candlestick chart generation (green/red)
- 🔔 Telegram alerts with image + caption
- 🕒 Auto-runs every 2 hours and sleeps
- 🛠️ Modular code (easy to extend or modify)

---

## 🧠 Strategy: Moving Average Crossover

A signal is triggered when:
- **Bullish:** Fast MA crosses **above** Slow MA
- **Bearish:** Fast MA crosses **below** Slow MA

---

## 🛠 Requirements

```bash
pip install -r requirements.txt
