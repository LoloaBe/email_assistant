"""
Content processor module for AI-powered email responses.
"""

import openai
import logging
from typing import Dict
import json
import requests
from email_handler import EmailConfig

class ContentProcessor:
    def __init__(self, config: EmailConfig):
        """Initialize the content processor."""
        self.config = config
        openai.api_key = config.openai_api_key
        
        # Load LLM configuration
        try:
            with open('llm_config.json', 'r') as f:
                self.llm_config = json.load(f)
        except Exception as e:
            logging.error(f"Error loading LLM configuration: {str(e)}")
            raise
        
    def generate_response_local(self, email_content: Dict) -> str:
        """Generate response using local LLama model."""
        try:
            # Create system prompt
            system_prompt = self.llm_config.get("system_prompt", "")
            
            if self.config.response_rules:
                system_prompt += "\nAdditional rules to follow:\n"
                for rule in self.config.response_rules:
                    system_prompt += f"- {rule}\n"
            
            # Create user prompt
            user_prompt = f"""
            Please respond to this email:
            
            From: {email_content['from']}
            Subject: {email_content['subject']}
            
            Content:
            {email_content['body']}
            """
            
            # Prepare the request
            url = f"{self.llm_config['local_model']['base_url']}/chat/completions"
            headers = {
                "Content-Type": "application/json"
            }
            data = {
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.7,
                "model": self.llm_config['local_model']['model']
            }
            
            # Make the request
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            
            # Extract the response
            result = response.json()
            generated_text = result['choices'][0]['message']['content'].strip()
            
            # Add model disclosure
            model_name = self.llm_config['local_model']['model']
            disclosure = f"\n\n---\nThis response was generated using the {model_name} language model running locally."
            
            return generated_text + disclosure
            
        except Exception as e:
            logging.error(f"Error generating response from local model: {str(e)}")
            raise

    def generate_response_openai(self, email_content: Dict) -> str:
        """Generate response using OpenAI's GPT."""
        try:
            # Create system prompt
            system_prompt = self.llm_config.get("system_prompt", "")
            
            if self.config.response_rules:
                system_prompt += "\nAdditional rules to follow:\n"
                for rule in self.config.response_rules:
                    system_prompt += f"- {rule}\n"
            
            # Create user prompt
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
            
            generated_text = response.choices[0].message.content.strip()
            
            # Add model disclosure
            model_name = "GPT-4"
            disclosure = f"\n\n---\nThis response was generated using the {model_name} language model."
            
            return generated_text + disclosure
            
        except Exception as e:
            logging.error(f"Error generating AI response: {str(e)}")
            raise

    def generate_response(self, email_content: Dict) -> str:
        """Generate response using configured model."""
        if self.llm_config.get("model_type", "local") == "local":
            return self.generate_response_local(email_content)
        else:
            return self.generate_response_openai(email_content)