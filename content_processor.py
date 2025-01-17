"""
Content processor module for AI-powered email responses.
"""

import openai
import logging
from typing import Dict
from email_handler import EmailConfig

class ContentProcessor:
    def __init__(self, config: EmailConfig):
        """Initialize the content processor."""
        self.config = config
        openai.api_key = config.openai_api_key
        
    def generate_response(self, email_content: Dict) -> str:
        """
        Generate AI response for an email.
        
        Args:
            email_content: Dictionary containing email information
                         (subject, body, from, etc.)
        
        Returns:
            str: Generated response
        """
        try:
            # Create system prompt with response rules
            system_prompt = """You are a professional email assistant. Your name is Luca.
            Generate responses that are:
            - Clear and concise
            - Professional yet friendly
            - Directly addressing the email's content
            - Using appropriate tone based on the original email
            - Sign emails as 'Luca'
            - Never include XML tags or style information
            """
            
            if self.config.response_rules:
                system_prompt += "\nAdditional rules to follow:\n"
                for rule in self.config.response_rules:
                    system_prompt += f"- {rule}\n"
            
            # Create user prompt from email content
            user_prompt = f"""
            Please respond to this email:
            
            From: {email_content['from']}
            Subject: {email_content['subject']}
            
            Content:
            {email_content['body']}
            """
            
            # Generate response using OpenAI
            client = openai.OpenAI(api_key=self.config.openai_api_key)
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logging.error(f"Error generating AI response: {str(e)}")
            raise