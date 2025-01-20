"""
Enhanced content processor module with business knowledge base integration.
"""

from src.core.email_handler import EmailConfig
import openai
import logging
from typing import Dict
import json
import requests
import os

class ContentProcessor:
    def __init__(self, config: EmailConfig):
        """Initialize the content processor."""
        self.config = config
        openai.api_key = config.openai_api_key
        
        business_config_path = 'config/business_config.json'
        
        # Load LLM configuration
        try:
            with open('config/llm_config.json', 'r') as f:
                self.llm_config = json.load(f)
        except Exception as e:
            logging.error(f"Error loading LLM configuration: {str(e)}")
            raise

        # Load business configuration
        try:
            if not os.path.exists(business_config_path):
                logging.error(f"Business configuration file not found: {business_config_path}")
                raise FileNotFoundError(f"Business configuration file not found: {business_config_path}")
                
            with open(business_config_path, 'r') as f:
                self.business_info = json.load(f)
            logging.info("Business configuration loaded successfully")
        except Exception as e:
            logging.error(f"Error loading business configuration: {str(e)}")
            raise

    def _enhance_system_prompt(self, base_prompt: str) -> str:
        """Enhance the system prompt with business knowledge."""
        business_context = f"""
        You are responding as a representative of {self.business_info['name']}.
        Location: {self.business_info['location']}
        Contact: Phone {self.business_info['contact']['phone']}

        Key Information:
        - We specialize in: {', '.join(self.business_info['specializations'])}
        - Current policy: {self.business_info['policies']['new_patients_2024_2025']}
        - Our staff: {', '.join(d['name'] for d in self.business_info['staff'])}

        Please use this information to provide accurate responses about our services and policies.
        """
        return base_prompt + "\n" + business_context

    def _categorize_email_intent(self, email_content: Dict) -> str:
        """Categorize the main intent of the email for targeted response."""
        subject = email_content['subject'].lower()
        body = email_content['body'].lower()
        
        keywords = {
            'appointment': ['appointment', 'booking', 'schedule', 'visit', 'termin'],
            'services': ['treatment', 'service', 'procedure', 'therapy', 'behandlung'],
            'costs': ['cost', 'price', 'fee', 'insurance', 'payment', 'kosten'],
            'information': ['information', 'details', 'question', 'inquiry', 'info'],
            'emergency': ['emergency', 'urgent', 'immediate', 'notfall']
        }
        
        for intent, words in keywords.items():
            if any(word in subject or word in body for word in words):
                return intent
                
        return 'general'

    def _create_context_for_intent(self, intent: str) -> str:
        """Create relevant context based on email intent."""
        contexts = {
            'appointment': f"""
                Booking Information:
                - Phone: {self.business_info['contact']['phone']}
                - Current Policy: {self.business_info['policies']['new_patients_2024_2025']}
            """,
            'services': f"""
                Our Services:
                - General Dermatology: {self.business_info['services']['general_dermatology']}
                - Aesthetic Treatments: {self.business_info['services']['aesthetic']}
                - Specialized Services: {self.business_info['services']['specialized']}
            """,
            'emergency': f"""
                For emergencies:
                - Contact us at {self.business_info['contact']['phone']}
                - Location: {self.business_info['location']}
            """
        }
        return contexts.get(intent, "")

    def generate_response_local(self, email_content: Dict) -> str:
        """Generate response using local LLama model with business knowledge."""
        try:
            # Enhance system prompt with business knowledge
            system_prompt = self._enhance_system_prompt(self.llm_config.get("system_prompt", ""))
            
            # Determine email intent and add relevant context
            intent = self._categorize_email_intent(email_content)
            additional_context = self._create_context_for_intent(intent)
            
            # Create user prompt with context
            user_prompt = f"""
            Please respond to this email with the following context:
            {additional_context}
            
            From: {email_content['from']}
            Subject: {email_content['subject']}
            
            Content:
            {email_content['body']}
            """
            
            # Prepare the request
            url = f"{self.llm_config['local_model']['base_url']}/chat/completions"
            headers = {"Content-Type": "application/json"}
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
            
            # Extract and format the response
            result = response.json()
            generated_text = result['choices'][0]['message']['content'].strip()
            
            return generated_text
            
        except Exception as e:
            logging.error(f"Error generating response from local model: {str(e)}")
            raise

    def generate_response_openai(self, email_content: Dict) -> str:
        """Generate response using OpenAI's GPT with business knowledge."""
        try:
            # Enhance system prompt with business knowledge
            system_prompt = self._enhance_system_prompt(self.llm_config.get("system_prompt", ""))
            
            # Determine email intent and add relevant context
            intent = self._categorize_email_intent(email_content)
            additional_context = self._create_context_for_intent(intent)
            
            # Create user prompt with context
            user_prompt = f"""
            Please respond to this email with the following context:
            {additional_context}
            
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

    def generate_response(self, email_content: Dict) -> str:
        """Generate response using configured model."""
        if self.llm_config.get("model_type", "local") == "local":
            return self.generate_response_local(email_content)
        else:
            return self.generate_response_openai(email_content)