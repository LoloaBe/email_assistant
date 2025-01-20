"""
Simple script to test IMAP and SMTP connections.
"""
import imaplib
import smtplib
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_email_connection(config_path="email_config.json"):
    """Test both IMAP and SMTP connections."""
    try:
        # Load config
        with open(config_path) as f:
            config = json.load(f)
        
        # Test IMAP
        logging.info(f"Testing IMAP connection to {config['imap_server']}...")
        imap = imaplib.IMAP4_SSL(config['imap_server'])
        imap.login(config['email_address'], config['email_password'])
        
        # List mailboxes
        mailboxes = imap.list()
        logging.info("Available mailboxes:")
        for mailbox in mailboxes[1]:
            logging.info(f"  {mailbox.decode()}")
        
        imap.logout()
        logging.info("IMAP connection successful!")
        
        # Test SMTP
        logging.info(f"\nTesting SMTP connection to {config['smtp_server']}:{config['smtp_port']}...")
        
        if config['smtp_port'] == 465:
            # Use SSL
            smtp = smtplib.SMTP_SSL(config['smtp_server'], config['smtp_port'])
        else:
            # Use STARTTLS
            smtp = smtplib.SMTP(config['smtp_server'], config['smtp_port'])
            smtp.starttls()
            
        smtp.login(config['email_address'], config['email_password'])
        smtp.quit()
        logging.info("SMTP connection successful!")
        
        print("\nAll connections tested successfully! ✓")
        
    except FileNotFoundError:
        print("\nError: email_config.json not found!")
        print("Please create email_config.json with your email settings.")
        print("\nExample format:")
        print("""{
    "email_address": "your-email@ionos.de",
    "email_password": "your-password",
    "imap_server": "imap.ionos.de",
    "smtp_server": "smtp.ionos.de",
    "smtp_port": 465
}""")
    except Exception as e:
        logging.error(f"Connection test failed: {str(e)}")

if __name__ == "__main__":
    test_email_connection()