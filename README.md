# YouTube Transcriber Bot

A Telegram bot that transcribes and summarizes YouTube videos using Mistral AI.

## Features

- Extracts video captions from YouTube
- Generates concise summaries using Mistral AI
- Handles errors gracefully
- Supports both local development and cloud deployment

## Deployment on Render

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Add environment variables:
   - `TELEGRAM_TOKEN`: Your Telegram bot token
   - `MISTRAL_API_KEY`: Your Mistral API key
   - `WEBHOOK_SECRET`: A random secret string (generate with `openssl rand -hex 32`)
   - `WEBHOOK_URL`: Will be provided by Render (format: https://your-app-name.onrender.com)

## Local Development

1. Create a `.env` file with:

## Setup

1. Clone the repository.
2. Install dependencies using `pip install -r requirements.txt`.
3. Set up your environment variables in a `.env` file.
4. Run the bot using `python src/bot.py`.

## Requirements

- Python 3.x
- Telegram Bot API token
- OpenAI API key

## Usage

Send a YouTube link to the bot, and it will reply with a summary of the video.

## License

This project is licensed under the MIT License.


deploying the bot on Google Cloud Run:

# Build for linux/amd64
docker buildx build --platform linux/amd64 `
    -t europe-west1-docker.pkg.dev/youtube-telegram-ai-summary/youtube-transcriber-bot/bot:latest .

# Push to registry
docker push europe-west1-docker.pkg.dev/youtube-telegram-ai-summary/youtube-transcriber-bot/bot:latest

# Deploy with simpler configuration
gcloud run deploy youtube-transcriber-bot `
    --image europe-west1-docker.pkg.dev/youtube-telegram-ai-summary/youtube-transcriber-bot/bot:latest `
    --platform managed `
    --region europe-west1 `
    --project youtube-telegram-ai-summary `
    --allow-unauthenticated `
    --min-instances 1 `
    --memory 512Mi `
    --timeout 300 `
    --set-env-vars="WEBHOOK_URL=https://youtube-transcriber-bot-oilexqkmpa-uc.a.run.app"
