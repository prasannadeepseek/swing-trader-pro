# alerts/telegram/signal_alerts.py
import telegram
from config.broker_config import TELEGRAM_CONFIG


class TelegramAlerts:
    def __init__(self):
        self.bot = telegram.Bot(token=TELEGRAM_CONFIG['token'])
        self.chat_id = TELEGRAM_CONFIG['chat_id']

    def send_signal(self, signal):
        """Send new trade signal alert"""
        message = self.format_signal_message(signal)
        self.bot.send_message(
            chat_id=self.chat_id,
            text=message,
            parse_mode="Markdown"
        )

    def format_signal_message(self, signal):
        """Format signal message with emojis"""
        return f"""
🎯 *NEW TRADE SIGNAL* 🚀
━━━━━━━━━━━━━━━━━━
• Symbol: `{signal['symbol']}`
• Direction: {signal['direction'].upper()}
• Entry: ₹{signal['entry']:.2f}
• SL: ₹{signal['sl']:.2f} ({signal['sl_pct']}%)
• Target: ₹{signal['target']:.2f} (+{signal['target_pct']}%)
━━━━━━━━━━━━━━━━━━
📊 Technical Score: {signal['score']}/10
⏳ Validity: {signal['validity']} days
"""
# method 2


class TelegramSignalAlerts:
    @staticmethod
    def new_swing_signal(signal):
        return f"""
🎯 *SWING SIGNAL* ({signal['trend'].upper()})
━━━━━━━━━━━━━━━━━━
• Symbol: {signal['symbol']}
• Weight: {signal['weight']:.2f}
• Entry: ₹{signal['entry']:.2f}
• SL: ₹{signal['sl']:.2f} ({signal['sl_pct']}%)
• Target: ₹{signal['target']:.2f} (+{signal['target_pct']}%)
• Validity: {signal['validity']}
━━━━━━━━━━━━━━━━━━
📊 Wyckoff Phase: {signal['wyckoff_phase']}
📈 Trend Strength: {signal['trend_strength']}/10
"""
