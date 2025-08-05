# data.py

import requests
import pandas as pd

def get_top_100_usdt_pairs():
    """
    Fetch top 100 USDT trading pairs by 24h volume from Binance.
    Filters for spot markets and excludes leveraged tokens and BUSD pairs.
    """
    url = "https://api.binance.com/api/v3/ticker/24hr"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Filter only USDT spot pairs, exclude leveraged tokens and BUSD
        usdt_pairs = [
            item for item in data
            if item["symbol"].endswith("USDT")
            and not item["symbol"].endswith("BUSD")
            and "UP" not in item["symbol"]
            and "DOWN" not in item["symbol"]
            and "BEAR" not in item["symbol"]
            and "BULL" not in item["symbol"]
        ]

        # Sort by quote volume descending and return top 200
        sorted_pairs = sorted(usdt_pairs, key=lambda x: float(x["quoteVolume"]), reverse=True)
        top_100_symbols = [item["symbol"] for item in sorted_pairs[:200]]

        return top_100_symbols

    except Exception as e:
        print(f"❌ [ERROR] Failed to fetch top 100 pairs: {e}")
        return []

def get_klines(symbol, interval="1h", limit=100):
    """
    Fetch candlestick (kline) data from Binance and return as a DataFrame.
    """
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data or len(data) < 2:
            raise ValueError("Insufficient candle data")

        df = pd.DataFrame(data, columns=[
            "timestamp", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "trades",
            "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
        ])

        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df = df[["timestamp", "open", "high", "low", "close", "volume"]].copy()
        df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float)
        return df

    except Exception as e:
        print(f"❌ [ERROR] {symbol}: Failed to fetch or parse candles — {e}")
        return pd.DataFrame()  # Return empty DataFrame to trigger skip
