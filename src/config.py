# src/config.py
import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        self.TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
        self.MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')
        self.WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET')
        self.WEBHOOK_URL = os.getenv('WEBHOOK_URL')
        
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