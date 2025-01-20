"""
Test script for basic email functionality.
"""

import logging
from src.core.email_handler import EmailConfig, EmailHandler
from src.core.email_monitor import EmailMonitor
from src.ai.content_processor import ContentProcessor

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_email_system():
    try:
        # Initialize components
        config = EmailConfig()
        monitor = EmailMonitor(config)
        processor = ContentProcessor(config)
        handler = EmailHandler(config)
        
        logging.info("Starting email system test...")
        
        # Check for new emails
        new_emails = monitor.check_new_emails()
        
        if new_emails:
            logging.info(f"Found {len(new_emails)} new email(s)")
            
            for email_data in new_emails:
                # Log email details
                logging.info("\nEmail Details:")
                logging.info(f"From: {email_data['from']}")
                logging.info(f"Subject: {email_data['subject']}")
                logging.info(f"Body: {email_data['body'][:200]}...")  # First 200 chars
                
                # Generate response
                response = processor.generate_response(email_data)
                logging.info(f"\nGenerated Response:\n{response}\n")
                
                # Send response
                handler.send_response(
                    to_address=email_data['from'],
                    subject=f"Re: {email_data['subject']}",
                    body=response
                )
                logging.info(f"Response sent to {email_data['from']}")
                
        else:
            logging.info("No new emails found")
            
        logging.info("Email system test completed successfully!")
        
    except Exception as e:
        logging.error(f"Test failed: {str(e)}")
        raise

if __name__ == "__main__":
    test_email_system()