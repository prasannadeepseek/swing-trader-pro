# alerts/email/urgent_alerts.py
from config.email_config import EMAIL_CONFIG
from typing import Optional
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

# method 2 final version


class UrgentAlerts(DailyDigest):
    """
    A class to send urgent position alerts via email, extending DailyDigest.
    """

    def __init__(
        self,
        smtp_server: Optional[str] = None,
        port: Optional[int] = None,
        sender: Optional[str] = None,
        password: Optional[str] = None,
        recipients: Optional[list] = None,
    ):
        """
        Initialize the UrgentAlerts email sender.

        Args:
            smtp_server (str, optional): SMTP server address. Defaults to EMAIL_CONFIG.
            port (int, optional): SMTP server port. Defaults to EMAIL_CONFIG.
            sender (str, optional): Sender email address. Defaults to EMAIL_CONFIG.
            password (str, optional): Sender email password. Defaults to EMAIL_CONFIG.
            recipients (list, optional): List of recipient email addresses. Defaults to EMAIL_CONFIG.
        """
        super().__init__(smtp_server, port, sender, password)
        self.recipients = recipients or EMAIL_CONFIG['alert_recipients']

    def send_position_alert(self, symbol: str, action: str, reason: str) -> bool:
        """
        Send an urgent position alert email.

        Args:
            symbol (str): The stock symbol.
            action (str): The action to be taken (e.g., BUY, SELL).
            reason (str): The reason for the alert.

        Returns:
            bool: True if email sent successfully, False otherwise.
        """
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
        try:
            return self.send(self.recipients, subject, content)
        except Exception as e:
            print(f"Failed to send urgent alert: {e}")
            return False
