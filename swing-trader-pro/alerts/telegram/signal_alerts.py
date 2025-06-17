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
# method 3
# alerts/telegram/signal_alerts.py


class InstitutionalAlert:
    @staticmethod
    def hedge_alert(symbol, hedge_type):
        return f"""
⚠️ *HEDGE DETECTED*: {symbol}
━━━━━━━━━━━━━━━━━━
Type: {hedge_type}
Action: Position size reduced
━━━━━━━━━━━━━━━━━━
"""

# method 4 final version


class TelegramAlerts:
    """
    Unified Telegram Alerts class for sending various trading signal notifications.
    """

    def __init__(self):
        self.bot = telegram.Bot(token=TELEGRAM_CONFIG['token'])
        self.chat_id = TELEGRAM_CONFIG['chat_id']

    def send_signal(self, signal):
        """
        Send a new trade signal alert after validating the signal.
        """
        if not self._validate_signal(signal, required_fields=[
            'symbol', 'direction', 'entry', 'sl', 'sl_pct', 'target', 'target_pct', 'score', 'validity'
        ]):
            raise ValueError(
                "Signal missing required fields for standard alert.")
        message = self.format_signal_message(signal)
        self._send_message(message)

    def send_swing_signal(self, signal):
        """
        Send a swing signal alert after validating the signal.
        """
        if not self._validate_signal(signal, required_fields=[
            'symbol', 'trend', 'weight', 'entry', 'sl', 'sl_pct', 'target', 'target_pct', 'validity', 'wyckoff_phase', 'trend_strength'
        ]):
            raise ValueError("Signal missing required fields for swing alert.")
        message = self.format_swing_signal_message(signal)
        self._send_message(message)

    def send_hedge_alert(self, symbol, hedge_type):
        """
        Send an institutional hedge alert.
        """
        message = self.format_hedge_alert(symbol, hedge_type)
        self._send_message(message)

    def _send_message(self, message):
        """
        Internal method to send a message to Telegram.
        """
        self.bot.send_message(
            chat_id=self.chat_id,
            text=message,
            parse_mode="Markdown"
        )

    @staticmethod
    def format_signal_message(signal):
        """
        Format standard trade signal message with emojis.
        """
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

    @staticmethod
    def format_swing_signal_message(signal):
        """
        Format swing signal message with Wyckoff and trend info.
        """
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

    @staticmethod
    def format_hedge_alert(symbol, hedge_type):
        """
        Format institutional hedge alert message.
        """
        return f"""
⚠️ *HEDGE DETECTED*: {symbol}
━━━━━━━━━━━━━━━━━━
Type: {hedge_type}
Action: Position size reduced
━━━━━━━━━━━━━━━━━━
"""

    @staticmethod
    def _validate_signal(signal, required_fields):
        """
        Validate that the signal dict contains all required fields.
        """
        return all(field in signal for field in required_fields)
