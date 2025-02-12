import os
import sys
import logging

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.bot import YouTubeBot

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

def main():
    try:
        port = int(os.environ.get('PORT', 8080))  # Render assigns this
        logger.info(f"Starting bot on port {port}")

        bot = YouTubeBot()
        if os.environ.get('RENDER'):
            logger.info("Running on Render - using webhook mode")
            webhook_url = os.environ.get('WEBHOOK_URL', f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}")
            bot.start_webhook(
                port=port, 
                webhook_url=webhook_url,
                listen="0.0.0.0"  # Ensure it binds correctly
            )
        else:
            logger.info("Running locally - using polling mode")
            bot.start_polling()
        
    except Exception as e:
        logger.error(f"Failed to start: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
