from .caption_handler import CaptionHandler
import logging

logger = logging.getLogger(__name__)

class YoutubeTranscriber:
    def __init__(self):
        self.caption_handler = CaptionHandler()

    def get_transcript(self, video_url: str) -> str:
        """Get transcript for a YouTube video"""
        try:
            video_id = self.caption_handler.extract_video_id(video_url)
            return self.caption_handler.get_transcript(video_id)
        except Exception as e:
            logger.error(f"Error getting transcript: {str(e)}")
            raise 