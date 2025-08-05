import asyncio
from telegram import Bot
from config import TELEGRAM_TOKEN, CHAT_ID

class Notifier:
    def __init__(self):
        self.bot = Bot(token=TELEGRAM_TOKEN)
        # Create a persistent event loop for the notifier
        try:
            self.loop = asyncio.get_event_loop()
            if self.loop.is_closed():
                self.loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self.loop)
        except RuntimeError:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)

    async def _send(self, symbol, signal_type, chart_buf):
        direction_emoji = "📈" if signal_type == 'bullish' else "📉"
        caption = (
            f"🔔 {symbol}\n"
            f"⚠️ MA Cross Detected in {symbol} for a possible  {signal_type.upper()}* {direction_emoji}* movement."
        )
        await self.bot.send_photo(
            chat_id=CHAT_ID,
            photo=chart_buf,
            caption=caption,
            parse_mode='Markdown'
        )

    def send_alert(self, symbol, signal_type, chart_buf):
        try:
            # Use the persistent event loop to run the coroutine
            if self.loop.is_running():
                asyncio.run_coroutine_threadsafe(
                    self._send(symbol, signal_type, chart_buf), self.loop
                ).result()
            else:
                self.loop.run_until_complete(self._send(symbol, signal_type, chart_buf))
        except Exception as e:
            print(f"❌ [NOTIFIER ERROR] {symbol}: {e}")

    def close(self):
        # Properly close the event loop if it's not already closed
        if self.loop and not self.loop.is_closed():
            self.loop.close()