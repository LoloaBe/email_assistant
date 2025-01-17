"""
Email Assistant Application
Continuously monitors emails and responds only to whitelisted senders.
"""

import time
import logging
from email_handler import EmailConfig, EmailHandler
from email_monitor import EmailMonitor
from content_processor import ContentProcessor
import re

class EmailAssistant:
    def __init__(self, config_path: str = "email_config.json"):
        """Initialize the email assistant application."""
        try:
            self.config = EmailConfig(config_path)
            self.monitor = EmailMonitor(self.config)
            self.processor = ContentProcessor(self.config)
            self.handler = EmailHandler(self.config)
            
            # Whitelist of allowed sender emails
            self.allowed_senders = ["l.criscuolo@gmx.com"]
            
            logging.info("Email Assistant initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize Email Assistant: {str(e)}")
            raise

    def extract_email_address(self, from_field: str) -> str:
        """Extract email address from the From field."""
        # Try to match email pattern
        match = re.search(r'[\w\.-]+@[\w\.-]+', from_field)
        if match:
            return match.group(0)
        return from_field

    def is_sender_allowed(self, from_field: str) -> bool:
        """Check if the sender is in the whitelist."""
        email_address = self.extract_email_address(from_field)
        return email_address in self.allowed_senders

    def process_emails(self):
        """Process new emails and respond to allowed senders."""
        try:
            new_emails = self.monitor.check_new_emails()
            
            for email_data in new_emails:
                sender = email_data['from']
                
                if self.is_sender_allowed(sender):
                    logging.info(f"Processing email from whitelisted sender: {sender}")
                    
                    # Generate response
                    response = self.processor.generate_response(email_data)
                    
                    # Send response
                    self.handler.send_response(
                        to_address=sender,
                        subject=f"Re: {email_data['subject']}",
                        body=response
                    )
                    logging.info(f"Response sent to {sender}")
                else:
                    logging.info(f"Skipping email from non-whitelisted sender: {sender}")
                    
        except Exception as e:
            logging.error(f"Error processing emails: {str(e)}")

    def run(self, check_interval: int = 60):
        """
        Run the email assistant with specified check interval.
        
        Args:
            check_interval: Time in seconds between email checks (default: 60)
        """
        logging.info(f"Starting Email Assistant (checking every {check_interval} seconds)")
        logging.info(f"Whitelisted senders: {', '.join(self.allowed_senders)}")
        
        while True:
            try:
                self.process_emails()
                time.sleep(check_interval)
                
            except KeyboardInterrupt:
                logging.info("Shutting down Email Assistant...")
                break
                
            except Exception as e:
                logging.error(f"Error in main loop: {str(e)}")
                logging.info("Waiting 60 seconds before retrying...")
                time.sleep(60)

def main():
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('email_assistant.log'),
            logging.StreamHandler()
        ]
    )
    
    try:
        assistant = EmailAssistant()
        assistant.run()
    except Exception as e:
        logging.critical(f"Application failed to start: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()