# src/summary_generator.py
import openai
from typing import Optional
import logging
from .exceptions import *
import time

logger = logging.getLogger(__name__)

class SummaryGenerator:
    def __init__(self, api_key: str):
        self.api_key = api_key
        openai.api_key = api_key
        self.max_retries = 3
        self.retry_delay = 1  # seconds

    def generate_summary(self, transcript: str, max_length: int = 4000) -> str:
        """
        Generate summary using OpenAI with error handling and rate limiting
        """
        if not transcript:
            raise ValueError("Empty transcript provided")

        # Truncate transcript if too long
        truncated_transcript = transcript[:max_length]
        retry_count = 0

        while retry_count < self.max_retries:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that provides concise video summaries and key insights."},
                        {"role": "user", "content": f"Please provide a summary and key insights from this transcript: {truncated_transcript}"}
                    ],
                    max_tokens=500,
                    temperature=0.7
                )

                return response.choices[0].message['content']

            except openai.error.RateLimitError:
                retry_count += 1
                if retry_count == self.max_retries:
                    raise RateLimitError("OpenAI API rate limit exceeded")
                logger.warning(f"Rate limit hit, retrying in {self.retry_delay} seconds...")
                time.sleep(self.retry_delay * retry_count)

            except openai.error.AuthenticationError:
                raise APIError("Invalid OpenAI API key")

            except openai.error.APIError as e:
                retry_count += 1
                if retry_count == self.max_retries:
                    raise APIError(f"OpenAI API error: {str(e)}")
                time.sleep(self.retry_delay)

            except Exception as e:
                logger.error(f"Error generating summary: {str(e)}")
                raise APIError(f"Failed to generate summary: {str(e)}")