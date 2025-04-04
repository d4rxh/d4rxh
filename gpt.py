import logging
import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import openai

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Environment variables se tokens load karein
TELEGRAM_TOKEN = os.getenv('8060825958:AAGItfzwc9lWu8F8k_0f1TN0Q4xvv5inRx4')
OPENAI_API_KEY = os.getenv('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')
if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
    logger.error("TELEGRAM_TOKEN ya OPENAI_API_KEY environment variables set nahi hain.")
    exit(1)

openai.api_key = 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

def start(update: Update, context: CallbackContext) -> None:
    """Start command ke response mein welcome message bhejta hai."""
    update.message.reply_text('Namaste! Main ChatGPT Telegram Bot hoon. Apna message bhejein.')

def chat(update: Update, context: CallbackContext) -> None:
    """User ke message ka response ChatGPT se leta hai aur reply karta hai."""
    user_message = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}],
            max_tokens=150
        )
        bot_reply = response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        bot_reply = "Maaf kijiye, mujhe aapka sawal samajhne mein dikkat ho rahi hai."

    update.message.reply_text(bot_reply)

def main():
    """Bot ko initialize aur start karta hai."""
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, chat))

    # Bot ko polling mode mein run karein (local run ke liye)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()