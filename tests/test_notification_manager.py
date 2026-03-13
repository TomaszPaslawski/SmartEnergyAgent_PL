import pytest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
from telegram.error import TelegramError
from src.notification_manager import send_telegram_message, _send_message_async


@patch('src.notification_manager.asyncio.run')
@patch('src.notification_manager.Bot')
@patch('src.notification_manager.os.getenv')
def test_send_telegram_message_success(mock_getenv, mock_bot, mock_asyncio_run):
    """Test of sending Telegram message - success."""

    # Mock for environment variables
    def getenv_side_effect(key):
        if key == "TELEGRAM_BOT_TOKEN":
            return "test_token_123"
        elif key == "TELEGRAM_CHAT_ID":
            return "test_chat_456"
        return None

    mock_getenv.side_effect = getenv_side_effect

    # Mock Bot (without error)
    mock_bot_instance = MagicMock()
    mock_bot.return_value = mock_bot_instance

    # Mock asyncio.run (simulate success)
    mock_asyncio_run.return_value = None

    result = send_telegram_message("Test message")

    assert result == True

    # Check if bot was called with token
    mock_bot.assert_called_once_with(token="test_token_123")

    # Check if asyncio.run was called
    mock_asyncio_run.assert_called_once()


@patch('src.notification_manager.os.getenv')
def test_send_telegram_message_no_token(mock_getenv):
    """Test lack of TELEGRAM_BOT_TOKEN."""

    # Mock getenv – token None, chat_id OK
    def getenv_side_effect(key):
        if key == "TELEGRAM_BOT_TOKEN":
            return None  # No token
        elif key == "TELEGRAM_CHAT_ID":
            return "test_chat_456"
        return None

    mock_getenv.side_effect = getenv_side_effect

    result = send_telegram_message("Test message")

    assert result == False


@patch('src.notification_manager.os.getenv')
def test_send_telegram_message_no_chat_id(mock_getenv):
    """Test lack of TELEGRAM_CHAT_ID."""

    # Mock getenv – token OK, chat_id None
    def getenv_side_effect(key):
        if key == "TELEGRAM_BOT_TOKEN":
            return "test_token_123"
        elif key == "TELEGRAM_CHAT_ID":
            return None  # No chat_id
        return None

    mock_getenv.side_effect = getenv_side_effect

    result = send_telegram_message("Test message")

    assert result == False


from telegram.error import TelegramError


@patch('src.notification_manager.asyncio.run')
@patch('src.notification_manager.Bot')
@patch('src.notification_manager.os.getenv')
def test_send_telegram_message_telegram_error(mock_getenv, mock_bot, mock_asyncio_run):
    """Test when Telegram API return error."""

    def getenv_side_effect(key):
        if key == "TELEGRAM_BOT_TOKEN":
            return "test_token_123"
        elif key == "TELEGRAM_CHAT_ID":
            return "test_chat_456"
        return None

    mock_getenv.side_effect = getenv_side_effect
    mock_bot_instance = MagicMock()
    mock_bot.return_value = mock_bot_instance

    mock_asyncio_run.side_effect = TelegramError("API error")

    result = send_telegram_message("Test message")

    assert result == False


@patch('src.notification_manager.asyncio.run')
@patch('src.notification_manager.Bot')
@patch('src.notification_manager.os.getenv')
def test_send_telegram_message_unexpected_error(mock_getenv, mock_bot, mock_asyncio_run):
    """Test for unexpected error."""

    # Mock for environment variables
    def getenv_side_effect(key):
        if key == "TELEGRAM_BOT_TOKEN":
            return "test_token_123"
        elif key == "TELEGRAM_CHAT_ID":
            return "test_chat_456"
        return None

    mock_getenv.side_effect = getenv_side_effect

    # Mock Bot
    mock_bot_instance = MagicMock()
    mock_bot.return_value = mock_bot_instance

    # Mock asyncio.run – unexpected error
    mock_asyncio_run.side_effect = Exception("Unexpected error")

    result = send_telegram_message("Test message")

    assert result == False


import asyncio
from src.notification_manager import _send_message_async


@patch('src.notification_manager.Bot')
def test_send_message_async_direct(mock_bot_class):
    """Direct test of function async _send_message_async."""

    mock_bot = MagicMock()
    mock_bot.send_message = AsyncMock(return_value=None)

    asyncio.run(_send_message_async(mock_bot, "test_chat_123", "Test message"))

    mock_bot.send_message.assert_called_once_with(
        chat_id="test_chat_123",
        text="Test message",
        parse_mode='HTML'
    )