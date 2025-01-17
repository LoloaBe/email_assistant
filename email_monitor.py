"""
Email monitoring module to handle incoming emails.
"""

import imaplib
import email
from typing import Dict, List
import logging
from email_handler import EmailConfig

class EmailMonitor:
    def __init__(self, config: EmailConfig):
        """Initialize email monitor with configuration."""
        self.config = config
        self._processed_ids = set()  # Keep track of processed email IDs

    def _connect_imap(self) -> imaplib.IMAP4_SSL:
        """Establish IMAP connection."""
        try:
            imap = imaplib.IMAP4_SSL(self.config.imap_server)
            imap.login(self.config.email_address, self.config.email_password)
            return imap
        except Exception as e:
            logging.error(f"Failed to connect to IMAP server: {str(e)}")
            raise

    def _parse_email(self, msg) -> Dict:
        """Parse email message into a structured format."""
        email_data = {
            'subject': msg['subject'] or '',
            'from': msg['from'] or '',
            'to': msg['to'] or '',
            'date': msg['date'] or '',
            'body': '',
            'message_id': msg['message-id'] or ''
        }

        # Get email body
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    try:
                        email_data['body'] = part.get_payload(decode=True).decode()
                        break
                    except:
                        continue
        else:
            try:
                email_data['body'] = msg.get_payload(decode=True).decode()
            except:
                email_data['body'] = msg.get_payload()

        return email_data

    def check_new_emails(self) -> List[Dict]:
        """Check for new unread emails."""
        new_emails = []
        try:
            # Connect to IMAP server
            imap = self._connect_imap()
            
            # Select inbox
            imap.select('INBOX')

            # Search for unread emails
            _, message_numbers = imap.search(None, 'UNSEEN')
            
            for num in message_numbers[0].split():
                try:
                    # Fetch email message
                    _, msg_data = imap.fetch(num, '(RFC822)')
                    email_body = msg_data[0][1]
                    msg = email.message_from_bytes(email_body)
                    
                    # Get message ID
                    message_id = msg['message-id']
                    
                    # Skip if already processed
                    if message_id in self._processed_ids:
                        continue
                    
                    # Parse email
                    email_data = self._parse_email(msg)
                    
                    # Add to processed set
                    self._processed_ids.add(message_id)
                    new_emails.append(email_data)
                    
                    # Mark as read
                    imap.store(num, '+FLAGS', '\\Seen')
                    
                    logging.info(f"Processed new email: {email_data['subject']}")
                    
                except Exception as e:
                    logging.error(f"Error processing individual email: {str(e)}")
                    continue
            
            imap.logout()
            
        except Exception as e:
            logging.error(f"Error checking emails: {str(e)}")
            raise
            
        return new_emails