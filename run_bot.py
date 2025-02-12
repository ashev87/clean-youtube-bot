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
        port = int(os.environ.get('PORT', 8080))
        logger.info(f"Starting application on port {port}")
        
        bot = YouTubeBot()
        bot.start_webhook(port)
        
    except Exception as e:
        logger.error(f"Failed to start: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main() 