# src/caption_handler.py
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable
)
import logging
from src.exceptions import *
import re
from youtube_transcript_api.formatters import TextFormatter

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='youtube_bot.log'
)
logger = logging.getLogger(__name__)

class CaptionHandler:
    def extract_video_id(self, url: str) -> str:
        """Extract video ID from YouTube URL"""
        patterns = [
            r'(?:v=|\/videos\/|embed\/|youtu.be\/|\/v\/|\/e\/|watch\?v%3D|watch\?feature=player_embedded&v=|%2Fvideos%2F|embed%\u200C\u200B2F|youtu.be%2F|%2Fv%2F)([^#\&\?\n]*)',
            r'(?:youtu\.be\/|youtube\.com(?:\/embed\/|\/v\/|\/watch\?v=|\/watch\?.+&v=))([\w-]{11})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                logger.info(f"Extracted video ID: {match.group(1)}")
                return match.group(1)
                
        logger.error(f"Could not extract video ID from URL: {url}")
        raise VideoNotFoundError("Could not extract video ID from URL")

    def get_transcript(self, video_id: str) -> str:
        """Get transcript from YouTube video"""
        try:
            logger.info(f"Fetching transcript for video ID: {video_id}")
            
            # Try to get transcript in English first
            try:
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                logger.info(f"Available transcripts: {transcript_list.manual}, {transcript_list.generated}")
                
                # Try to get English transcript
                try:
                    transcript = transcript_list.find_transcript(['en'])
                except:
                    # If no English transcript, try to translate to English
                    transcript = transcript_list.find_manually_created_transcript()
                    transcript = transcript.translate('en')
                    
            except Exception as e:
                logger.error(f"Error getting transcript list: {str(e)}")
                # Fallback to direct transcript fetch
                transcript = YouTubeTranscriptApi.get_transcript(video_id)
            
            # Format transcript
            formatter = TextFormatter()
            formatted_transcript = formatter.format_transcript(transcript)
            
            logger.info(f"Successfully got transcript of length: {len(formatted_transcript)}")
            return formatted_transcript

        except Exception as e:
            logger.error(f"Error getting transcript: {str(e)}")
            if "No transcript found" in str(e):
                raise TranscriptNotAvailableError("No captions available for this video")
            raise VideoNotFoundError("Could not access video")