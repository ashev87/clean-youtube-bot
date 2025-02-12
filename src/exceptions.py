# src/exceptions.py
class YouTubeBotError(Exception):
    """Base exception class for YouTube Bot"""
    pass

class VideoNotFoundError(YouTubeBotError):
    """Raised when video cannot be found"""
    pass

class TranscriptNotAvailableError(YouTubeBotError):
    """Raised when transcript is not available"""
    pass

class APIError(YouTubeBotError):
    """Raised when API calls fail"""
    pass

class RateLimitError(YouTubeBotError):
    """Raised when hitting API rate limits"""
    pass