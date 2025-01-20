"""
Test script to compare responses with and without business knowledge base.
"""

import logging
import sys
import os
import json

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, project_root)

from src.core.email_handler import EmailConfig
from src.ai.content_processor import ContentProcessor

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class ContentProcessorNoKnowledge(ContentProcessor):
    """A modified version of ContentProcessor that doesn't use business knowledge"""
    def __init__(self, config: EmailConfig):
        self.config = config
        self.openai_api_key = config.openai_api_key
        
        # Load LLM configuration only
        try:
            config_path = os.path.join(project_root, 'config', 'llm_config.json')
            with open(config_path, 'r') as f:
                self.llm_config = json.load(f)
        except Exception as e:
            logging.error(f"Error loading LLM configuration: {str(e)}")
            raise
            
        # Initialize empty business info
        self.business_info = {}

    def _enhance_system_prompt(self, base_prompt: str) -> str:
        """Override to provide minimal context"""
        return base_prompt

    def _create_context_for_intent(self, intent: str) -> str:
        """Override to provide no additional context"""
        return ""

def test_knowledge_base_comparison():
    try:
        # Initialize base configuration
        config = EmailConfig()
        
        # Complex test case that requires detailed knowledge
        test_email = {
            "from": "patient@example.com",
            "subject": "Multiple Treatment Questions",
            "body": """
            Hello,
            
            I have several questions about your services:
            1. I have severe acne and am interested in both the dermatology treatment and laser therapy. Which of your doctors specializes in both?
            2. Do you currently accept new patients with public insurance for these treatments?
            3. For the laser treatment, is Dr. Bachmann available this month?
            4. Do you also treat hyperhidrosis, and if yes, what methods do you use?
            
            Thank you for your help,
            Maria
            """
        }
        
        # Test 1: With Knowledge Base
        logging.info("\n=== Test with Business Knowledge Base ===")
        processor_with_knowledge = ContentProcessor(config)
        response_with_knowledge = processor_with_knowledge.generate_response(test_email)
        
        # Test 2: Without Knowledge Base
        logging.info("\n=== Test without Business Knowledge Base ===")
        processor_without_knowledge = ContentProcessorNoKnowledge(config)
        response_without_knowledge = processor_without_knowledge.generate_response(test_email)
        
        # Display results
        logging.info("\n" + "="*50)
        logging.info("ORIGINAL EMAIL:")
        logging.info(f"Subject: {test_email['subject']}")
        logging.info(f"Body:\n{test_email['body']}")
        
        logging.info("\n" + "="*50)
        logging.info("RESPONSE WITH KNOWLEDGE BASE:")
        logging.info("-"*50)
        logging.info(response_with_knowledge)
        
        logging.info("\n" + "="*50)
        logging.info("RESPONSE WITHOUT KNOWLEDGE BASE:")
        logging.info("-"*50)
        logging.info(response_without_knowledge)
        
        logging.info("\n" + "="*50)
        
    except Exception as e:
        logging.error(f"Test failed: {str(e)}")
        raise

if __name__ == "__main__":
    test_knowledge_base_comparison()