"""
Test script for email monitoring functionality with detailed logging.
"""

import logging
from src.core.email_handler import EmailConfig
from src.core.email_monitor import EmailMonitor
import time

logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG for more detailed output
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
            logging.info(f"\nFound {len(new_emails)} new email(s)!")
            
            # Print details of each new email
            for i, email in enumerate(new_emails, 1):
                logging.info(f"\nEmail {i} Details:")
                logging.info("=" * 50)
                logging.info(f"From: {email['from']}")
                logging.info(f"Subject: {email['subject']}")
                logging.info(f"Date: {email['date']}")
                logging.info("\nBody Content:")
                logging.info("-" * 50)
                logging.info(f"{email['body']}")
                logging.info("=" * 50 + "\n")
        else:
            logging.info("No new emails found.")
            
        logging.info("Email monitor test completed successfully!")
        
    except Exception as e:
        logging.error(f"Failed to test email monitor: {str(e)}")
        raise

if __name__ == "__main__":
    test_email_monitor()