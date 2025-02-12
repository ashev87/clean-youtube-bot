# src/bot.py
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from telegram import Update
import logging
from src.caption_handler import CaptionHandler
from src.mistral_summary_generator import MistralSummaryGenerator
from src.config import Config
from src.exceptions import *
import json
import traceback
import os
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

class YouTubeBot:
    def __init__(self):
        self.config = Config()
        self.caption_handler = CaptionHandler()
        self.summary_generator = MistralSummaryGenerator(self.config.MISTRAL_API_KEY)
        self.app = Application.builder().token(self.config.TELEGRAM_TOKEN).build()

    async def handle_error(self, update: Update, error_message: str):
        """Handle errors and send user-friendly messages"""
        logger.error(f"Error for user {update.effective_user.id}: {error_message}")
        await update.message.reply_text(
            f"❌ {error_message}\n\nPlease try again or contact support if the issue persists.",
            parse_mode='Markdown'
        )

    async def handle_youtube_link(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming YouTube links with comprehensive error handling"""
        try:
            url = update.message.text

            # Send processing message
            processing_message = await update.message.reply_text(
                "🔄 Processing your video... Please wait.",
                parse_mode='Markdown'
            )

            try:
                video_id = self.caption_handler.extract_video_id(url)
            except VideoNotFoundError as e:
                await self.handle_error(update, "Invalid YouTube URL. Please check the link and try again.")
                return

            try:
                transcript = self.caption_handler.get_transcript(video_id)
            except TranscriptNotAvailableError:
                await self.handle_error(update, "No captions available for this video. Try another video.")
                return
            except VideoNotFoundError:
                await self.handle_error(update, "Video is unavailable or private.")
                return

            try:
                summary = self.summary_generator.generate_summary(transcript)
            except RateLimitError:
                await self.handle_error(update, "Service is busy. Please try again in a few minutes.")
                return
            except APIError as e:
                await self.handle_error(update, f"Error generating summary: {str(e)}")
                return

            # Delete processing message
            await processing_message.delete()

            # Send summary
            message = f"📺 *Video Summary*\n\n{summary}\n\n🔗 [Original Video]({url})"
            await update.message.reply_text(
                message,
                parse_mode='Markdown',
                disable_web_page_preview=True
            )

        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            await self.handle_error(update, "An unexpected error occurred. Please try again later.")

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        await update.message.reply_text(
            "👋 Hi! Send me a YouTube link and I'll summarize it for you!",
            parse_mode='Markdown'
        )

    def start_polling(self):
        """Start the bot with polling (for local testing)"""
        try:
            # Add handlers
            self.app.add_handler(MessageHandler(
                filters.TEXT & (filters.Entity("url") | filters.Regex(r'youtube\.com|youtu\.be')),
                self.handle_youtube_link
            ))
            self.app.add_handler(MessageHandler(filters.COMMAND, self.start_command))

            logger.info("Starting bot in polling mode")
            self.app.run_polling()

        except Exception as e:
            logger.critical(f"Failed to start bot: {str(e)}")
            raise

    def start_webhook(self):
        """Start the bot with webhook"""
        port = int(os.environ.get('PORT', 8080))
        webhook_url = os.environ.get('WEBHOOK_URL', f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}")
        
        print(f"Starting webhook on port {port}", file=sys.stdout)
        print(f"Webhook URL: {webhook_url}", file=sys.stdout)
        
        self._add_handlers()

        self.app.run_webhook(
            listen="0.0.0.0",
            port=port,
            webhook_url=webhook_url,  # Simplified URL
            drop_pending_updates=True
        )

    def _add_handlers(self):
        """Add message handlers"""
        self.app.add_handler(MessageHandler(
            filters.TEXT & (filters.Entity("url") | filters.Regex(r'youtube\.com|youtu\.be')),
            self.handle_youtube_link
        ))
        self.app.add_handler(MessageHandler(filters.COMMAND, self.start_command))