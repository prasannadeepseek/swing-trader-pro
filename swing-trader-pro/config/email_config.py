# config/email_config.py
EMAIL_SETTINGS = {
    "smtp_server": "smtp.gmail.com",
    "port": 587,
    "sender": "your_email@gmail.com",
    "password": "your_password",
    "alert_recipients": ["recipient1@email.com"]
}
# method 3 final version
# config/email_config.py

"""
Email configuration for alerting and notifications.

Edit this file to update SMTP settings and recipients.
"""

EMAIL_CONFIG = {
    "smtp_server": "smtp.gmail.com",
    "port": 587,
    "use_tls": True,  # Set to False if using SSL or no encryption
    "use_ssl": False,  # Set to True if using SSL (e.g., port 465)
    "sender": "your_email@gmail.com",
    "password": "your_password",
    "alert_recipients": ["recipient1@email.com"],
    # Optional fields:
    "cc": [],
    "bcc": [],
}
