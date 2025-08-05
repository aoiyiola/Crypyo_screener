# main.py

import time
import atexit
import threading
from config import SHORT_MA, LONG_MA, TIMEFRAME, INTERVAL_HOURS
from data import get_top_100_usdt_pairs, get_klines
from indicators import detect_crossover
from plotter import plot_chart
from notifier import Notifier

notifier = Notifier()
atexit.register(notifier.close)

def run_scan():
    print("🚀 Starting market scan...")
    pairs = get_top_100_usdt_pairs()
    if not pairs:
        print("⚠️ No pairs retrieved from Binance.")
        return

    for symbol in pairs:
        try:
            df = get_klines(symbol, interval=TIMEFRAME)
            if df.empty or len(df) < LONG_MA + 2:
                print(f"⏭️ Skipping {symbol}: Not enough data")
                continue

            signal = detect_crossover(df, SHORT_MA, LONG_MA)
            if signal:
                chart = plot_chart(df, symbol, SHORT_MA, LONG_MA)
                notifier.send_alert(symbol, signal, chart)
                print(f"✅ Alert sent for {symbol}: {signal.upper()} crossover")
        except Exception as e:
            print(f"❌ [ERROR] {symbol}: {e}")

if __name__ == "__main__":
    try:
    
        while True:
            run_scan()
            print(f"😴 Sleeping for {INTERVAL_HOURS} hours...\n")
            time.sleep(INTERVAL_HOURS * 60 * 60)

    except KeyboardInterrupt:
        print("\n🛑 Script terminated by user (Ctrl+C). Cleaning up...")
    except Exception as e:
        print(f"\n💥 Unhandled exception: {e}")
    finally:
        notifier.close()
