"""
Email parsing module for handling different email formats and content types.
"""

import email
from email.header import decode_header
from typing import Dict
import logging
from bs4 import BeautifulSoup
import re
import quopri
import base64

class EmailParser:
    @staticmethod
    def decode_email_field(field: str) -> str:
        """Decode email field with proper character encoding."""
        if not field:
            return ""
            
        decoded_parts = []
        for part, encoding in decode_header(field):
            if isinstance(part, bytes):
                try:
                    decoded_parts.append(part.decode(encoding or 'utf-8'))
                except:
                    decoded_parts.append(part.decode('utf-8', 'ignore'))
            else:
                decoded_parts.append(str(part))
        return ' '.join(decoded_parts)

    @staticmethod
    def decode_payload(part) -> str:
        """Decode email payload handling various encodings."""
        content = ""
        if part.get('Content-Transfer-Encoding') == 'base64':
            try:
                payload = part.get_payload(decode=True)
                if payload:
                    charset = part.get_content_charset() or 'utf-8'
                    content = payload.decode(charset, 'replace')
            except:
                try:
                    content = base64.b64decode(part.get_payload()).decode('utf-8', 'replace')
                except:
                    content = part.get_payload()
        elif part.get('Content-Transfer-Encoding') == 'quoted-printable':
            try:
                payload = part.get_payload(decode=True)
                if payload:
                    charset = part.get_content_charset() or 'utf-8'
                    content = payload.decode(charset, 'replace')
            except:
                try:
                    content = quopri.decodestring(part.get_payload().encode()).decode('utf-8', 'replace')
                except:
                    content = part.get_payload()
        else:
            try:
                payload = part.get_payload(decode=True)
                if payload:
                    charset = part.get_content_charset() or 'utf-8'
                    content = payload.decode(charset, 'replace')
            except:
                content = part.get_payload()
                
        return content.strip()

    @staticmethod
    def clean_html(html_content: str) -> str:
        """Clean HTML content and extract readable text."""
        try:
            # Remove HTML comments
            html_content = re.sub(r'<!--.*?-->', '', html_content, flags=re.DOTALL)
            
            # Create BeautifulSoup object
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Remove unwanted tags
            for tag in soup(['script', 'style', 'meta', 'link', 'head']):
                tag.decompose()
                
            # Handle special cases for links
            for a in soup.find_all('a'):
                href = a.get('href', '')
                text = a.get_text().strip()
                # Only keep the link if it's different from the text
                if href and text and href != text:
                    a.replace_with(f"{text} ({href})")
                else:
                    a.replace_with(text or href)
            
            # Replace line breaks with newlines
            for br in soup.find_all(['br', 'p']):
                br.replace_with('\n' + br.get_text() + '\n')
            
            # Get text and clean it
            text = soup.get_text()
            
            # Clean up whitespace and empty lines
            lines = []
            for line in text.split('\n'):
                line = line.strip()
                if line and not line.startswith('http') and not line.startswith('https'):
                    lines.append(line)
            
            return '\n'.join(lines)
            
        except Exception as e:
            logging.error(f"Error cleaning HTML: {str(e)}")
            # Fallback to basic cleaning
            text = re.sub(r'<[^>]+>', ' ', html_content)
            text = re.sub(r'\s+', ' ', text)
            return text.strip()

    @staticmethod
    def parse_email_message(msg) -> Dict:
        """Parse email message into a structured format."""
        email_data = {
            'subject': '',
            'from': '',
            'to': '',
            'date': '',
            'body': '',
            'message_id': ''
        }
        
        # Parse headers
        email_data['subject'] = EmailParser.decode_email_field(msg.get('subject', ''))
        email_data['from'] = EmailParser.decode_email_field(msg.get('from', ''))
        email_data['to'] = EmailParser.decode_email_field(msg.get('to', ''))
        email_data['date'] = msg.get('date', '')
        email_data['message_id'] = msg.get('message-id', '')

        # Extract body content
        text_content = []
        
        if msg.is_multipart():
            # First pass: look for text/plain parts
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    content = EmailParser.decode_payload(part)
                    if content:
                        text_content.append(content)
            
            # Second pass: if no text/plain found, look for text/html
            if not text_content:
                for part in msg.walk():
                    if part.get_content_type() == 'text/html':
                        content = EmailParser.decode_payload(part)
                        if content:
                            cleaned_content = EmailParser.clean_html(content)
                            if cleaned_content:
                                text_content.append(cleaned_content)
        else:
            content = EmailParser.decode_payload(msg)
            if msg.get_content_type() == 'text/html':
                content = EmailParser.clean_html(content)
            if content:
                text_content.append(content)
        
        # Combine and clean up content
        if text_content:
            combined_text = '\n\n'.join(text_content)
            # Remove excessive whitespace
            combined_text = re.sub(r'\n\s*\n', '\n\n', combined_text)
            # Remove URL-only lines
            lines = [line.strip() for line in combined_text.splitlines()]
            filtered_lines = [line for line in lines if line and not line.startswith(('http://', 'https://'))]
            email_data['body'] = '\n'.join(filtered_lines).strip()
            
        return email_data