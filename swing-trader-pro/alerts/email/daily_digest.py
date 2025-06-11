# alerts/email/daily_digest.py
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
