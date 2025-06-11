# alerts/email/urgent_alerts.py
from email.daily_digest import DailyDigest
from datetime import datetime
# from config.email_config import EMAIL_CONFIG
from config import email_config


class UrgentAlerts(DailyDigest):
    def send_position_alert(self, symbol, action, reason):
        subject = f"URGENT: {action.upper()} {symbol}"
        content = f"""
        <html>
            <body>
                <h2>Action Required</h2>
                <p>Symbol: <strong>{symbol}</strong></p>
                <p>Action: <strong>{action}</strong></p>
                <p>Reason: {reason}</p>
                <p>Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </body>
        </html>
        """
        self.send(
            email_config.EMAIL_CONFIG['alert_recipients'], subject, content)
