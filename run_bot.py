import os
import sys
import logging
import traceback

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.bot import YouTubeBot

# Update logging config to write to both file and stdout
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('bot.log')
    ]
)
logger = logging.getLogger(__name__)

# Add immediate print statements for debugging
def main():
    try:
        print("Bot starting...", file=sys.stdout)
        print("Environment:", os.environ.get('RENDER'), os.environ.get('TELEGRAM_TOKEN'), file=sys.stdout)
        
        port = int(os.environ.get('PORT', 8080))
        print(f"Port: {port}", file=sys.stdout)
        
        print("Creating bot instance...", file=sys.stdout)
        bot = YouTubeBot()
        print("Bot instance created", file=sys.stdout)

        if os.environ.get('RENDER'):
            print("Configuring webhook...", file=sys.stdout)
            webhook_url = os.environ.get('WEBHOOK_URL', f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}")
            print(f"Webhook URL: {webhook_url}", file=sys.stdout)
            
            print("Starting webhook...", file=sys.stdout)
            bot.start_webhook(
                port=port, 
                webhook_url=webhook_url
            )
            print("Webhook started", file=sys.stdout)
        else:
            print("Starting polling...", file=sys.stdout)
            bot.start_polling()
        
    except Exception as e:
        print(f"CRITICAL ERROR: {str(e)}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
