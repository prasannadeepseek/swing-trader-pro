# alerts/email/daily_digest.py
from typing import List, Optional
import smtplib
from email.mime.text import MIMEText
from config.broker_config import EMAIL_CONFIG


class DailyDigest:
    def __init__(self):
        self.smtp_server = EMAIL_CONFIG['smtp_server']
        self.port = EMAIL_CONFIG['port']
        self.sender = EMAIL_CONFIG['sender']
        self.password = EMAIL_CONFIG['password']

    def send(self, recipients, subject, content):
        msg = MIMEText(content, 'html')
        msg['Subject'] = subject
        msg['From'] = self.sender
        msg['To'] = ', '.join(recipients)

        with smtplib.SMTP(self.smtp_server, self.port) as server:
            server.starttls()
            server.login(self.sender, self.password)
            server.send_message(msg)

# method 2 final version


class DailyDigest:
    """
    A class to send daily digest emails using SMTP.
    """

    def __init__(
        self,
        smtp_server: Optional[str] = None,
        port: Optional[int] = None,
        sender: Optional[str] = None,
        password: Optional[str] = None,
    ):
        """
        Initialize the DailyDigest email sender.

        Args:
            smtp_server (str, optional): SMTP server address. Defaults to EMAIL_CONFIG.
            port (int, optional): SMTP server port. Defaults to EMAIL_CONFIG.
            sender (str, optional): Sender email address. Defaults to EMAIL_CONFIG.
            password (str, optional): Sender email password. Defaults to EMAIL_CONFIG.
        """
        self.smtp_server = smtp_server or EMAIL_CONFIG['smtp_server']
        self.port = port or EMAIL_CONFIG['port']
        self.sender = sender or EMAIL_CONFIG['sender']
        self.password = password or EMAIL_CONFIG['password']

    def send(self, recipients: List[str], subject: str, content: str) -> bool:
        """
        Send an email to the specified recipients.

        Args:
            recipients (List[str]): List of recipient email addresses.
            subject (str): Email subject.
            content (str): Email content (HTML).

        Returns:
            bool: True if email sent successfully, False otherwise.
        """
        msg = MIMEText(content, 'html')
        msg['Subject'] = subject
        msg['From'] = self.sender
        msg['To'] = ', '.join(recipients)

        try:
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls()
                server.login(self.sender, self.password)
                server.sendmail(self.sender, recipients, msg.as_string())
            return True
        except Exception as e:
            # Optionally, log the exception here
            print(f"Failed to send email: {e}")
            return False
