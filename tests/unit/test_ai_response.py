"""
Test script for AI email response generation.
"""

import logging
import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, project_root)

from src.core.email_handler import EmailConfig
from src.ai.content_processor import ContentProcessor
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_ai_response():
    try:
        # Load configuration
        config = EmailConfig("config/email_config.json")
        processor = ContentProcessor(config)
        
        # Rest of your test code stays exactly the same
        test_emails = [
            {
                "from": "client@example.com",
                "subject": "Project Timeline Question",
                "body": """
                Hi there,
                
                I was wondering about the estimated completion date for the current phase 
                of our project. Could you provide an update on the progress and timeline?
                
                Thanks,
                John
                """
            },
            {
                "from": "support@example.com",
                "subject": "Technical Issue Report",
                "body": """
                Hello,
                
                I'm experiencing issues with the login system. The page keeps refreshing 
                and won't accept my credentials. This is urgent as I need to access the 
                system for a client demo tomorrow.
                
                Best regards,
                Sarah
                """
            }
        ]
        
        # Test response generation for each scenario
        for i, email in enumerate(test_emails, 1):
            logging.info(f"\nTesting scenario {i}:")
            logging.info(f"From: {email['from']}")
            logging.info(f"Subject: {email['subject']}")
            logging.info(f"Body: {email['body']}\n")
            
            response = processor.generate_response(email)
            
            logging.info("Generated response:")
            logging.info(f"{response}\n")
            logging.info("-" * 50)
        
        logging.info("AI response testing completed successfully!")
        
    except Exception as e:
        logging.error(f"Failed to test AI response: {str(e)}")
        raise  # Added to see the full error trace

if __name__ == "__main__":
    test_ai_response()