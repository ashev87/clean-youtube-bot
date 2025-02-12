# src/config.py
import os
from dotenv import load_dotenv
from google.cloud import secretmanager

class Config:
    def __init__(self):
        # Check if running locally
        is_local = not os.getenv('K_REVISION')
        
        if is_local:
            # Local development - use environment variables
            self.TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
            self.MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')
            self.WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET')
            self.WEBHOOK_URL = os.getenv('WEBHOOK_URL')
            self.TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
        else:
            # Cloud environment - use Secret Manager
            self.TELEGRAM_TOKEN = self._get_secret("youtube-bot-telegram-token")
            self.MISTRAL_API_KEY = self._get_secret("youtube-bot-mistral-api-key")
            self.WEBHOOK_SECRET = self._get_secret("youtube-bot-webhook-secret")
            self.WEBHOOK_URL = os.getenv('WEBHOOK_URL')
            self.TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

        # Validate required environment variables
        self.validate_config()

    def validate_config(self):
        required_vars = [
            'TELEGRAM_TOKEN', 
            'MISTRAL_API_KEY',
            'WEBHOOK_SECRET'
        ]
        missing_vars = [var for var in required_vars
                       if getattr(self, var) is None]

        if missing_vars:
            raise ValueError(f"Missing required variables: {missing_vars}")

    def _get_secret(self, secret_id):
        try:
            client = secretmanager.SecretManagerServiceClient()
            name = f"projects/youtube-telegram-ai-summary/secrets/{secret_id}/versions/latest"
            response = client.access_secret_version(request={"name": name})
            return response.payload.data.decode("UTF-8")
        except Exception as e:
            raise ValueError(f"Failed to get secret {secret_id}: {str(e)}")