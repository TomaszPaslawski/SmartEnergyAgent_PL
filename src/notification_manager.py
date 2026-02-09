import os
from dotenv import load_dotenv
import logging
from telegram import Bot
from telegram.error import TelegramError
from datetime import datetime
import asyncio

load_dotenv()

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# --- Helper function for running asynchronous operations ---
# Python-telegram-bot uses asyncio. A traditional synchronous function (like send_telegram_message)
# must use asyncio.run() to run the coroutine.
async def _send_message_async(bot: Bot, chat_id: str, message_text: str):
    await bot.send_message(chat_id=chat_id, text=message_text, parse_mode='HTML')


def send_telegram_message(message_text: str) -> bool:
    """
   Sends a text message via the Telegram bot.

    Args: message_text (str): The text of the message to send.

    Returns: bool: True if the message was sent successfully, False otherwise.

    """
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not bot_token:
        logger.error("TELEGRAM_BOT_TOKEN not found in .env. Cannot send message.")
        return False
    if not chat_id:
        logger.error("TELEGRAM_CHAT_ID not found in .env. Cannot send message.")
        return False

    try:
        bot = Bot(token=bot_token)
        logger.info(f"Attempting to send message to chat_id {chat_id}...")

        asyncio.run(_send_message_async(bot, chat_id, message_text))

        logger.info("Telegram message sent successfully.")
        return True
    except TelegramError as e:
        logger.error(f"Error sending Telegram message: {e}")
        return False
    except Exception as e:
        logger.error(f"An unexpected error occurred while sending Telegram message: {e}")
        return False


# Test section
if __name__ == "__main__":
    print("\n--- Running standalone test for notification_manager.py ---")

    test_message = "Hello from Smart Energy Agent! This is a test message. " \
                   "<b>Current time:</b> " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + \
                   "\n<i>This message should be formatted in HTML.</i>"

    print("Attempting to send test Telegram message...")
    success = send_telegram_message(test_message)
    if success:
        print("Test message sent. Check your Telegram chat.")
    else:
        print("Failed to send test message. Check logs for errors.")
    print("--- Test finished ---")