# Email Assistant

An AI-powered email assistant that automatically monitors and responds to emails using either OpenAI's GPT model or a local LLM (like Llama) through LM Studio.

## Features

- Continuous email monitoring
- Automated AI-powered responses using either:
  - OpenAI's GPT model
  - Local LLM through LM Studio
- Whitelist system for allowed senders
- Secure email handling with SSL support
- Comprehensive logging system
- Support for both IMAP and SMTP protocols

## Prerequisites

- Python 3.7+
- A valid OpenAI API key (if using OpenAI's model)
- LM Studio running locally (if using local LLM)
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

4. Configure your email settings:
```bash
cp email_config.example.json email_config.json
```

5. Edit `email_config.json` with your email credentials:
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

6. Set up your whitelist:
```bash
cp whitelist_config.example.json whitelist_config.json
```

7. Edit `whitelist_config.json` with allowed email addresses:
```json
{
    "allowed_senders": [
        "allowed-email1@example.com",
        "allowed-email2@example.com"
    ]
}
```

8. Configure your LLM settings:
```bash
cp llm_config.example.json llm_config.json
```

9. Edit `llm_config.json` to choose between local LLM or OpenAI:
```json
{
    "model_type": "local",  // or "openai"
    "local_model": {
        "base_url": "http://localhost:1234/v1",
        "model": "llama"
    },
    "system_prompt": "You are a professional email assistant..."
}
```

## Using Local LLM

1. Download and install LM Studio
2. Start your local server in LM Studio
3. Make sure your server is running on http://localhost:1234
4. Set "model_type": "local" in llm_config.json

## Using OpenAI

1. Ensure you have a valid OpenAI API key
2. Set "model_type": "openai" in llm_config.json
3. Add your OpenAI API key to email_config.json

## Usage

1. Start the email assistant:
```bash
python main.py
```

2. The assistant will:
   - Monitor your inbox for new emails
   - Process emails from whitelisted senders
   - Generate AI-powered responses using the configured model
   - Send automated replies
   - Log all activities to `email_assistant.log`

3. To stop the assistant, press `Ctrl+C`

## Configuration Files

### email_config.json
- Email credentials and server settings
- OpenAI API key (if using OpenAI)
- Response rules for the AI

### whitelist_config.json
- List of email addresses allowed to receive automated responses

### llm_config.json
- Choice of AI model (local or OpenAI)
- Local model settings
- System prompt for the AI

## Project Structure

```
email_assistant/
├── main.py                 # Main application entry point
├── email_handler.py        # Email sending/receiving functionality
├── email_monitor.py        # Email monitoring system
├── content_processor.py    # AI response generation
├── requirements.txt        # Python dependencies
├── email_config.json       # Email configuration
├── whitelist_config.json   # Allowed senders list
├── llm_config.json        # LLM configuration
└── tests/
    ├── test_basic_email.py
    ├── test_connection.py
    └── test_monitor.py
```

## Security Notes

- Never commit configuration files with real credentials
- Use environment variables in production
- Consider using app-specific passwords
- Regularly rotate your API keys and passwords
- Keep your local LLM server secure

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please open an issue in the GitHub repository.