# Email Assistant

An AI-powered email assistant that automatically monitors and responds to emails using OpenAI's GPT model.

## Features

- Continuous email monitoring
- Automated AI-powered responses using GPT
- Whitelist system for allowed senders
- Secure email handling with SSL support
- Comprehensive logging system
- Support for both IMAP and SMTP protocols

## Prerequisites

- Python 3.7+
- A valid OpenAI API key
- An email account with IMAP/SMTP access

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/email_assistant.git
cd email_assistant
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Create your configuration file:
```bash
cp email_config.example.json email_config.json
```

5. Edit `email_config.json` with your email and OpenAI credentials:
```json
{
    "email_address": "your-email@example.com",
    "email_password": "your-password",
    "imap_server": "imap.your-provider.com",
    "imap_port": 993,
    "imap_use_ssl": true,
    "smtp_server": "smtp.your-provider.com",
    "smtp_port": 465,
    "smtp_use_ssl": true,
    "openai_api_key": "your-openai-api-key",
    "response_rules": [
        "Always start with a warm greeting",
        "Use a professional but friendly tone",
        "Address the sender's concerns specifically",
        "End with a polite signature"
    ]
}
```

## Usage

1. Start the email assistant:
```bash
python main.py
```

2. The assistant will:
   - Monitor your inbox for new emails
   - Process emails from whitelisted senders
   - Generate AI-powered responses
   - Send automated replies
   - Log all activities to `email_assistant.log`

3. To stop the assistant, press `Ctrl+C`

## Configuration

### Email Settings

- `email_address`: Your email address
- `email_password`: Your email password or app-specific password
- `imap_server`: IMAP server address
- `imap_port`: IMAP port (usually 993 for SSL)
- `smtp_server`: SMTP server address
- `smtp_port`: SMTP port (usually 465 for SSL or 587 for TLS)

### AI Response Settings

The assistant uses GPT to generate responses. You can customize the response behavior by modifying the `response_rules` in the config file.

### Whitelist Configuration

By default, the assistant only responds to emails from whitelisted addresses. To modify the whitelist, edit the `allowed_senders` list in `main.py`:

```python
self.allowed_senders = ["allowed-email@example.com"]
```

## Testing

The repository includes several test scripts:

1. Test basic email functionality:
```bash
python test_basic_email.py
```

2. Test connection settings:
```bash
python test_connection.py
```

3. Test email monitoring:
```bash
python test_monitor.py
```

## Project Structure

```
email_assistant/
├── main.py                 # Main application entry point
├── email_handler.py        # Email sending/receiving functionality
├── email_monitor.py        # Email monitoring system
├── content_processor.py    # AI response generation
├── requirements.txt        # Python dependencies
├── email_config.json       # Configuration file
└── tests/
    ├── test_basic_email.py
    ├── test_connection.py
    └── test_monitor.py
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Security Note

- Never commit your `email_config.json` with real credentials
- Use environment variables or secure secret management in production
- Consider using app-specific passwords when available
- Regularly rotate your API keys and passwords

## Support

For support, please open an issue in the GitHub repository.