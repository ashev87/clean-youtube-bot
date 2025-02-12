import os
import sys
import logging

# Add src directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.bot import YouTubeBot

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

def main():
    try:
        # Render sets PORT environment variable, default is 10000
        port = int(os.environ.get('PORT', 10000))
        logger.info(f"Starting bot on port {port}")
        
        bot = YouTubeBot()
        if os.environ.get('RENDER'):
            logger.info("Running on Render - using webhook mode")
            bot.start_webhook(
                port=port,  # Use the port Render provides
                webhook_url=os.environ.get('WEBHOOK_URL')
            )
        else:
            logger.info("Running locally - using polling mode")
            bot.start_polling()
        
    except Exception as e:
        logger.error(f"Failed to start: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main() 