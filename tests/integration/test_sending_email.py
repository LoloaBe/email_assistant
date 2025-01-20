"""
Simple script to test sending an email through IONOS.
"""

import logging
from email_handler import EmailConfig, EmailHandler
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_send_email():
    try:
        # Load configuration
        config = EmailConfig()
        handler = EmailHandler(config)

        # Create test email content
        test_subject = "Test Email"
        test_body = f"""
        This is a test email sent from your Python email assistant.
        Time sent: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        If you receive this email, your email sending configuration is working correctly!
        """

        # Send the email
        logging.info("Attempting to send test email...")
        handler.send_response(
            to_address=config.email_address,  # Sending to self for testing
            subject=test_subject,
            body=test_body
        )
        logging.info("Test email sent successfully!")

    except Exception as e:
        logging.error(f"Failed to send test email: {str(e)}")

if __name__ == "__main__":
    test_send_email()