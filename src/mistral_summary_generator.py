from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import logging
from src.exceptions import *

logger = logging.getLogger(__name__)

class MistralSummaryGenerator:
    def __init__(self, api_key: str):
        self.client = MistralClient(api_key=api_key)
        self.model = "mistral-large-latest"

    def generate_summary(self, transcript: str, max_length: int = 4000) -> str:
        """Generate summary from transcript"""
        if not transcript:
            logger.error("Empty transcript provided")
            raise ValueError("Empty transcript provided")

        try:
            logger.info(f"Generating summary for transcript of length: {len(transcript)}")
            
            # Truncate transcript if too long
            if len(transcript) > max_length:
                logger.info(f"Truncating transcript from {len(transcript)} to {max_length} characters")
                transcript = transcript[:max_length]

            messages = [
                ChatMessage(role="user", content=f"Please provide a summary and key insights from this transcript: {transcript}")
            ]

            chat_response = self.client.chat(
                model=self.model,
                messages=messages
            )
            
            summary = chat_response.choices[0].message.content
            logger.info(f"Generated summary of length: {len(summary)}")
            return summary

        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            if "rate limit" in str(e).lower():
                raise RateLimitError("Rate limit exceeded")
            raise APIError(f"Failed to generate summary: {str(e)}") 