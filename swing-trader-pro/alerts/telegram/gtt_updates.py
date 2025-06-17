# alerts/telegram/gtt_updates.py
from telegram import ParseMode
from datetime import datetime
from alerts.telegram.signal_alerts import TelegramAlerts


class GTTUpdateAlerts:
    TEMPLATE = """
🔄 *GTT Order Updated*: {symbol}
━━━━━━━━━━━━━━━━━━
• New SL: ₹{sl:.2f} ({sl_change:+.1%})
• New Target: ₹{target:.2f} ({target_change:+.1%})
• Reason: {reason}
"""

    def send_update(self, symbol, sl, target, prev_sl, prev_target, reason):
        message = self.TEMPLATE.format(
            symbol=symbol,
            sl=sl,
            target=target,
            sl_change=(sl - prev_sl)/prev_sl,
            target_change=(target - prev_target)/prev_target,
            reason=reason
        )
        TelegramAlerts().send_message(message)

# method 2 final version


class GTTUpdateAlerts:
    """
    Sends GTT order update alerts to Telegram using the TelegramAlerts class.
    """

    TEMPLATE = """
🔄 *GTT Order Updated*: {symbol}
━━━━━━━━━━━━━━━━━━
• New SL: ₹{sl:.2f} ({sl_change:+.1%})
• New Target: ₹{target:.2f} ({target_change:+.1%})
• Reason: {reason}
• Time: {time}
"""

    def __init__(self):
        self.telegram_alerts = TelegramAlerts()

    def send_update(self, symbol: str, sl: float, target: float, prev_sl: float, prev_target: float, reason: str) -> None:
        """
        Send a GTT order update alert to Telegram.

        Args:
            symbol (str): The stock symbol.
            sl (float): The new stop loss value.
            target (float): The new target value.
            prev_sl (float): The previous stop loss value.
            prev_target (float): The previous target value.
            reason (str): The reason for the update.
        """
        try:
            sl_change = (sl - prev_sl) / prev_sl if prev_sl else 0.0
            target_change = (target - prev_target) / \
                prev_target if prev_target else 0.0
            message = self.TEMPLATE.format(
                symbol=symbol,
                sl=sl,
                target=target,
                sl_change=sl_change,
                target_change=target_change,
                reason=reason,
                time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
            self.telegram_alerts._send_message(message)
        except Exception as e:
            # Optionally log the error
            print(f"Failed to send GTT update alert: {e}")
