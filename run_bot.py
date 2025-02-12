import os
import sys
import logging

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
        print("Bot starting...", file=sys.stdout)  # Direct print for immediate feedback
        print("Environment:", os.environ.get('RENDER'), os.environ.get('TELEGRAM_TOKEN'), file=sys.stdout)
        
        port = int(os.environ.get('PORT', 8080))
        print(f"Port: {port}", file=sys.stdout)
        logger.info(f"Starting bot on port {port}")

        bot = YouTubeBot()
        if os.environ.get('RENDER'):
            logger.info("Running on Render - using webhook mode")
            webhook_url = os.environ.get('WEBHOOK_URL', f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}")
            bot.start_webhook(
                port=port, 
                webhook_url=webhook_url
            )
        else:
            logger.info("Running locally - using polling mode")
            bot.start_polling()
        
    except Exception as e:
        logger.error(f"Failed to start: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
