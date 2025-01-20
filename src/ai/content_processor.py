"""
Enhanced content processor module with business knowledge base integration.
"""

from src.core.email_handler import EmailConfig
import openai
import logging
from typing import Dict, List, Union
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
        # First check if services exist and have the expected structure
        services = self.business_info.get('services', {})
        
        business_context = f"""
        You are responding as a representative of {self.business_info.get('name', '')}.
        Contact: Phone {self.business_info.get('contact', {}).get('phone', '')}, 
        Website: {self.business_info.get('contact', {}).get('website', '')}

        Key Information:
        - We specialize in: {', '.join(self.business_info.get('specializations', []))}
        
        Our Services:
        """
        
        # Add services if they exist
        if services:
            business_context += f"""
            - General Dermatology: {self._format_services(services.get('general_dermatology', {}))}
            - Skin Cancer: {self._format_services(services.get('skin_cancer', {}))}
            - Aesthetic: {self._format_services(services.get('aesthetic', {}))}
            - Specialized: {self._format_services(services.get('specialized', {}))}
            - Allergology: {services.get('allergology', '')}
            """

        business_context += f"""
        Staff:
        {self._format_staff(self.business_info.get('staff', []))}

        Policies:
        {self._format_policies(self.business_info.get('policies', {}))}

        Additional Information:
        {self.business_info.get('additional', '')}

        Please use this information to provide accurate responses about our services and policies.
        """
        return base_prompt + "\n" + business_context

    def _format_services(self, services: Union[Dict, str]) -> str:
        """Format services that can be either a dictionary or a string."""
        if isinstance(services, str):
            return services
        if not services:
            return ""
        return '; '.join([f"{key}: {value}" for key, value in services.items()])

    def _format_staff(self, staff: List[Dict]) -> str:
        """Format staff list into readable text."""
        if not staff:
            return "No staff information available."
        return '\n'.join([
            f"- {member['name']} (Specialties: {', '.join(member['specialties'])})"
            for member in staff
        ])

    def _format_policies(self, policies: Dict) -> str:
        """Format policies dictionary into readable text."""
        if not policies:
            return "No specific policies."
        return '\n'.join([f"- {key.replace('_', ' ').title()}: {value}" 
                         for key, value in policies.items()])

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
                - Contact: {self.business_info['contact']['phone']}
                - Website: {self.business_info['contact']['website']}
                {self._format_policies(self.business_info['policies'])}
                {self.business_info['additional']}
            """,
            'services': f"""
                Our Services:
                General Dermatology:
                {self._format_services(self.business_info['services']['general_dermatology'])}
                
                Aesthetic Treatments:
                {self._format_services(self.business_info['services']['aesthetic'])}
                
                Specialized Services:
                {self._format_services(self.business_info['services']['specialized'])}
                
                Allergology:
                {self.business_info['services']['allergology']}
            """,
            'emergency': f"""
                For emergencies:
                - Contact us at {self.business_info['contact']['phone']}
                - Website: {self.business_info['contact']['website']}
                
                Our Staff:
                {self._format_staff(self.business_info['staff'])}
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