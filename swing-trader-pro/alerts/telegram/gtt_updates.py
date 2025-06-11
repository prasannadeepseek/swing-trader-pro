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
