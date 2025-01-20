"""
Email Handler Module
Handles all email operations including configuration, fetching, and sending emails.
"""

import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from typing import List, Dict
import json
import logging
from datetime import datetime
import os
class EmailConfig:
    def __init__(self, config_path: str = "config/email_config.json"):
        """Initialize email configuration from JSON file."""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            # Required fields
            required_fields = [
                "email_address", "email_password", 
                "smtp_server", "smtp_port",
                "imap_server", "imap_port",
                "openai_api_key"
            ]
            
            missing_fields = [field for field in required_fields if field not in config]
            if missing_fields:
                raise KeyError(f"Missing required configuration fields: {', '.join(missing_fields)}")
            
            # Email settings
            self.email_address = config["email_address"]
            self.email_password = config["email_password"]
            
            # SMTP settings
            self.smtp_server = config["smtp_server"]
            self.smtp_port = config["smtp_port"]
            self.smtp_use_ssl = config.get("smtp_use_ssl", self.smtp_port == 465)
            
            # IMAP settings
            self.imap_server = config["imap_server"]
            self.imap_port = config["imap_port"]
            self.imap_use_ssl = config.get("imap_use_ssl", True)
            
            # OpenAI and response settings
            self.openai_api_key = config["openai_api_key"]
            self.response_rules = config.get("response_rules", [])
            
            logging.info("Email configuration loaded successfully")
            
        except Exception as e:
            logging.error(f"Error loading configuration: {str(e)}")
            raise

class EmailHandler:
    def __init__(self, config: EmailConfig):
        """Initialize the email handler with configuration."""
        self.config = config
    
    def send_response(self, to_address: str, subject: str, body: str):
        """Send email response."""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config.email_address
            msg['To'] = to_address
            msg['Subject'] = subject
            msg['Date'] = email.utils.formatdate(localtime=True)
            
            msg.attach(MIMEText(body, 'plain'))
            
            if self.config.smtp_use_ssl:
                # Use SSL for port 465
                smtp = smtplib.SMTP_SSL(self.config.smtp_server, self.config.smtp_port)
            else:
                # Use STARTTLS for port 587
                smtp = smtplib.SMTP(self.config.smtp_server, self.config.smtp_port)
                smtp.starttls()
            
            smtp.login(self.config.email_address, self.config.email_password)
            smtp.send_message(msg)
            smtp.quit()
            
            logging.info(f"Email sent successfully to {to_address}")
            
        except Exception as e:
            logging.error(f"Error sending email: {str(e)}")
            raise