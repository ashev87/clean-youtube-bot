# src/caption_handler.py
import yt_dlp
import sys
import traceback
from urllib.parse import urlparse, parse_qs
from .exceptions import VideoNotFoundError, TranscriptNotAvailableError
import os
import tempfile

class CaptionHandler:
    def __init__(self):
        # Get cookies from environment variable and parse them
        cookie_data = os.environ.get('YOUTUBE_COOKIES', '')
        cookie_header = ''
        
        # Parse cookie file format into header
        for line in cookie_data.split('\n'):
            if line and not line.startswith('#') and not line.startswith('.'):
                try:
                    domain, _, path, secure, expiry, name, value = line.strip().split('\t')
                    if domain in ('youtube.com', '.youtube.com', 'www.youtube.com'):
                        cookie_header += f"{name}={value}; "
                except Exception as e:
                    print(f"Error parsing cookie line: {e}", file=sys.stderr)
        
        self.ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': ['en'],
            'skip_download': True,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Cookie': cookie_header.strip(),
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-User': '?1',
                'Sec-Fetch-Dest': 'document',
                'sec-ch-ua': '"Not A(Brand";v="99", "Brave";v="121", "Chromium";v="121"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"'
            }
        }
        print(f"Initialized with headers: {self.ydl_opts['http_headers']}", file=sys.stdout)

    def get_transcript(self, video_id: str) -> str:
        try:
            print(f"Attempting to get transcript for video {video_id}", file=sys.stdout)
            url = f"https://www.youtube.com/watch?v={video_id}"
            
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                print("Getting video info...", file=sys.stdout)
                info = ydl.extract_info(url, download=False)
                
                if 'subtitles' in info and 'en' in info['subtitles']:
                    print("Found manual English subtitles", file=sys.stdout)
                    subtitles = info['subtitles']['en']
                elif 'automatic_captions' in info and 'en' in info['automatic_captions']:
                    print("Found auto-generated English subtitles", file=sys.stdout)
                    subtitles = info['automatic_captions']['en']
                else:
                    print("No English subtitles found", file=sys.stderr)
                    raise TranscriptNotAvailableError

                # Get the transcript text
                transcript = []
                for sub in subtitles:
                    if isinstance(sub, dict) and 'text' in sub:
                        transcript.append(sub['text'])
                
                full_transcript = ' '.join(transcript)
                print(f"Transcript length: {len(full_transcript)} chars", file=sys.stdout)
                return full_transcript

        except yt_dlp.utils.DownloadError as e:
            print(f"Download error: {str(e)}", file=sys.stderr)
            raise VideoNotFoundError
        except Exception as e:
            print(f"Unexpected error getting transcript: {str(e)}", file=sys.stderr)
            traceback.print_exc()
            raise VideoNotFoundError

    def extract_video_id(self, url: str) -> str:
        try:
            print(f"Attempting to extract video ID from URL: {url}", file=sys.stdout)
            if "youtu.be" in url:
                video_id = url.split("/")[-1].split("?")[0]
            else:
                parsed_url = urlparse(url)
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