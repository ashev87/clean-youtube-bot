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
import sys
import time
import traceback
from urllib.parse import urlparse, parse_qs
import httpx

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='youtube_bot.log'
)
logger = logging.getLogger(__name__)

class CaptionHandler:
    def extract_video_id(self, url: str) -> str:
        """Extract video ID from YouTube URL"""
        try:
            print(f"Attempting to extract video ID from URL: {url}", file=sys.stdout)
            # Try different URL patterns
            if "youtu.be" in url:
                video_id = url.split("/")[-1].split("?")[0]
            else:
                parsed_url = urlparse(url)
                print(f"Parsed URL: {parsed_url}", file=sys.stdout)
                if parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
                    if parsed_url.path == '/watch':
                        params = parse_qs(parsed_url.query)
                        video_id = params['v'][0]
                    else:
                        video_id = parsed_url.path.split("/")[-1]
                else:
                    raise VideoNotFoundError
                
            print(f"Successfully extracted video ID: {video_id}", file=sys.stdout)
            return video_id
        except Exception as e:
            print(f"Error extracting video ID: {str(e)}", file=sys.stderr)
            traceback.print_exc()
            raise VideoNotFoundError

    def get_transcript(self, video_id: str) -> str:
        """Get transcript from YouTube video"""
        try:
            print(f"Attempting to get transcript for video {video_id}", file=sys.stdout)
            time.sleep(1)
            
            # Add headers to mimic a browser
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            # Create a custom http client
            http_client = httpx.Client(
                headers=headers,
                follow_redirects=True
            )
            
            try:
                print("Attempting to list transcripts...", file=sys.stdout)
                transcript_list = YouTubeTranscriptApi.list_transcripts(
                    video_id,
                    http_client=http_client
                )
                print("Got transcript list", file=sys.stdout)
                
                # Try to get manual transcripts first, then auto-generated
                try:
                    transcript = transcript_list.find_manually_created_transcript()
                    print("Found manual transcript", file=sys.stdout)
                except NoTranscriptFound:
                    transcript = transcript_list.find_generated_transcript()
                    print("Found auto-generated transcript", file=sys.stdout)
                
                transcript_data = transcript.fetch()
                print("Successfully fetched transcript data", file=sys.stdout)
                
            except TranscriptsDisabled as e:
                print(f"Transcripts disabled: {str(e)}", file=sys.stderr)
                raise TranscriptNotAvailableError
            except NoTranscriptFound as e:
                print(f"No transcript found: {str(e)}", file=sys.stderr)
                raise TranscriptNotAvailableError
            except VideoUnavailable as e:
                print(f"Video unavailable: {str(e)}", file=sys.stderr)
                raise VideoNotFoundError
            except Exception as e:
                print(f"Failed to get transcript: {str(e)}", file=sys.stderr)
                traceback.print_exc()
                raise VideoNotFoundError

            # Join all transcript pieces
            full_transcript = ' '.join([entry['text'] for entry in transcript_data])
            print(f"Transcript length: {len(full_transcript)} chars", file=sys.stdout)
            
            return full_transcript
        
        except Exception as e:
            print(f"Unexpected error getting transcript: {str(e)}", file=sys.stderr)
            traceback.print_exc()
            if isinstance(e, (TranscriptsDisabled, NoTranscriptFound)):
                raise TranscriptNotAvailableError
            raise VideoNotFoundError