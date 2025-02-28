"""
Test script for email monitoring functionality.
"""

import logging
import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, project_root)

from src.core.email_handler import EmailConfig
from src.core.email_monitor import EmailMonitor
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_email_monitor():
    try:
        # Load configuration
        config = EmailConfig()
        monitor = EmailMonitor(config)
        
        logging.info("Starting email monitor test...")
        logging.info("Checking for new emails...")
        
        # Check for new emails
        new_emails = monitor.check_new_emails()
        
        if new_emails:
            logging.info(f"Found {len(new_emails)} new email(s)!")
            
            # Print details of each new email
            for i, email in enumerate(new_emails, 1):
                logging.info(f"\nEmail {i}:")
                logging.info(f"From: {email['from']}")
                logging.info(f"Subject: {email['subject']}")
                logging.info(f"Date: {email['date']}")
                logging.info("Body preview: " + email['body'][:100] + "...")
                logging.info("-" * 50)
        else:
            logging.info("No new emails found.")
            
        logging.info("Email monitor test completed successfully!")
        
    except Exception as e:
        logging.error(f"Failed to test email monitor: {str(e)}")
        raise

if __name__ == "__main__":
    test_email_monitor()