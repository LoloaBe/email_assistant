"""
Test script for business-aware email responses.
Tests different types of inquiries to verify proper context inclusion.
"""

import logging
from email_handler import EmailConfig
from content_processor import ContentProcessor
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_responses():
    try:
        # Initialize configurations
        config = EmailConfig()
        processor = ContentProcessor(config)
        
        # Test cases covering different scenarios
        test_emails = [
            {
                "from": "test@example.com",
                "subject": "Appointment Request",
                "body": """
                Hello,
                
                I would like to schedule an appointment for a skin consultation.
                Do you accept new patients with public insurance?
                
                Best regards,
                Anna Schmidt
                """
            },
            {
                "from": "test2@example.com",
                "subject": "Question about treatments",
                "body": """
                Hi,
                
                I'm interested in your acne treatment services.
                Could you tell me what treatments you offer and how long they typically take?
                
                Thanks,
                Michael
                """
            },
            {
                "from": "test3@example.com",
                "subject": "Emergency Case",
                "body": """
                Hello,
                
                I have a severe allergic reaction on my face that started an hour ago.
                Do you accept emergency cases? What should I do?
                
                Regards,
                Thomas
                """
            },
            {
                "from": "test4@example.com",
                "subject": "Cost Inquiry",
                "body": """
                Good morning,
                
                I'm interested in laser treatment for spider veins.
                Could you provide information about the costs and if insurance covers it?
                
                Best regards,
                Julia
                """
            }
        ]
        
        # Test response generation for each scenario
        for i, email in enumerate(test_emails, 1):
            logging.info(f"\n{'='*50}")
            logging.info(f"Testing scenario {i}:")
            logging.info(f"From: {email['from']}")
            logging.info(f"Subject: {email['subject']}")
            logging.info(f"Body: {email['body'].strip()}")
            logging.info(f"{'-'*50}")
            
            # Generate response
            response = processor.generate_response(email)
            
            logging.info("\nGenerated response:")
            logging.info(f"{'-'*50}")
            logging.info(response)
            logging.info(f"{'='*50}\n")
            
            # Add a brief pause between tests for readability
            input("Press Enter to continue to next test case...\n")
        
        logging.info("All test scenarios completed successfully!")
        
    except Exception as e:
        logging.error(f"Test failed: {str(e)}")
        raise

if __name__ == "__main__":
    test_responses()