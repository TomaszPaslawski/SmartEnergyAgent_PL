import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from src.telegram_bot_handlers import (
    start_command,
    set_location_command,
    receive_city,
    cancel_command,
    status_command,
    create_bot_application,
    WAITING_FOR_CITY,
    ConversationHandler
)
import asyncio


def create_mock_update(user_id="123", first_name="Tomek", message_text="Warszawa"):
    """Helper – creates object's mock Update."""
    mock_update = MagicMock()
    mock_update.effective_user.id = user_id
    mock_update.effective_user.first_name = first_name
    mock_update.message.text = message_text
    mock_update.message.reply_text = AsyncMock()
    return mock_update


# --- /start ---

@patch('src.telegram_bot_handlers.get_location')
def test_start_command_new_user(mock_get_location):
    """Test /start for new usee (no location)."""
    mock_get_location.return_value = None

    mock_update = create_mock_update()
    mock_context = MagicMock()

    result = asyncio.run(start_command(mock_update, mock_context))

    # Should ask for location
    mock_update.message.reply_text.assert_called_once()
    call_text = mock_update.message.reply_text.call_args.args[0]
    assert "Welcome" in call_text
    assert "city" in call_text.lower()

    # Should move to the state WAITING_FOR_CITY
    assert result == WAITING_FOR_CITY


@patch('src.telegram_bot_handlers.get_location')
def test_start_command_existing_user(mock_get_location):
    """Test /start for user with saved location."""
    mock_get_location.return_value = (52.23, 21.01, "Warszawa")

    mock_update = create_mock_update()
    mock_context = MagicMock()

    result = asyncio.run(start_command(mock_update, mock_context))

    # Should shown existing location
    call_text = mock_update.message.reply_text.call_args.args[0]
    assert "Warszawa" in call_text
    assert "again" in call_text.lower()

    # Should end conversation
    assert result == ConversationHandler.END


# --- /set_location ---

def test_set_location_command():
    """Test /set_location – ask for city."""
    mock_update = create_mock_update()
    mock_context = MagicMock()

    result = asyncio.run(set_location_command(mock_update, mock_context))

    # Should ask for city
    mock_update.message.reply_text.assert_called_once()
    call_text = mock_update.message.reply_text.call_args.args[0]
    assert "city" in call_text.lower()

    # Should move to state WAITING_FOR_CITY
    assert result == WAITING_FOR_CITY


# --- receive_city ---

@patch('src.telegram_bot_handlers.save_location')
@patch('src.telegram_bot_handlers.validate_coordinates')
@patch('src.telegram_bot_handlers.geocode_city')
def test_receive_city_success(mock_geocode, mock_validate, mock_save):
    """Test city received – success (geocoding + saving)."""
    mock_geocode.return_value = (52.23, 21.01, "Warszawa, województwo mazowieckie, Polska")
    mock_validate.return_value = True
    mock_save.return_value = True

    mock_update = create_mock_update(message_text="Warszawa")
    mock_context = MagicMock()

    result = asyncio.run(receive_city(mock_update, mock_context))

    # Should save location
    mock_save.assert_called_once_with("123", 52.23, 21.01, "Warszawa")

    # Should end conversation
    assert result == ConversationHandler.END


@patch('src.telegram_bot_handlers.geocode_city')
def test_receive_city_not_found(mock_geocode):
    """Test city received – city not found."""
    mock_geocode.return_value = None

    mock_update = create_mock_update(message_text="XYZ123")
    mock_context = MagicMock()

    result = asyncio.run(receive_city(mock_update, mock_context))

    # Should ask for re-typing of the city
    call_args_list = mock_update.message.reply_text.call_args_list
    last_call_text = call_args_list[-1].args[0]
    assert "not found" in last_call_text

    # Should stay in state WAITING_FOR_CITY
    assert result == WAITING_FOR_CITY


@patch('src.telegram_bot_handlers.validate_coordinates')
@patch('src.telegram_bot_handlers.geocode_city')
def test_receive_city_invalid_coordinates(mock_geocode, mock_validate):
    """Test city received – wrong coordinates."""
    mock_geocode.return_value = (999, 999, "Incorrect city")
    mock_validate.return_value = False

    mock_update = create_mock_update(message_text="Incorrect city")
    mock_context = MagicMock()

    result = asyncio.run(receive_city(mock_update, mock_context))

    # Should ask for re-typing
    call_args_list = mock_update.message.reply_text.call_args_list
    last_call_text = call_args_list[-1].args[0]
    assert "Incorrect" in last_call_text

    # Should stay in the status WAITING_FOR_CITY
    assert result == WAITING_FOR_CITY


@patch('src.telegram_bot_handlers.save_location')
@patch('src.telegram_bot_handlers.validate_coordinates')
@patch('src.telegram_bot_handlers.geocode_city')
def test_receive_city_save_error(mock_geocode, mock_validate, mock_save):
    """Test city received – error while saving in database."""
    mock_geocode.return_value = (52.23, 21.01, "Warszawa")
    mock_validate.return_value = True
    mock_save.return_value = False  # Saving error

    mock_update = create_mock_update(message_text="Warszawa")
    mock_context = MagicMock()

    result = asyncio.run(receive_city(mock_update, mock_context))

    # Shuold inform about error
    call_args_list = mock_update.message.reply_text.call_args_list
    last_call_text = call_args_list[-1].args[0]
    assert "error" in last_call_text.lower() or "Occurred" in last_call_text

    # Should end conversation
    assert result == ConversationHandler.END


# --- /cancel ---

def test_cancel_command():
    """Test /cancel – conversation canceling."""
    mock_update = create_mock_update()
    mock_context = MagicMock()

    result = asyncio.run(cancel_command(mock_update, mock_context))

    # Shuold inform about canceling
    mock_update.message.reply_text.assert_called_once()
    call_text = mock_update.message.reply_text.call_args.args[0]
    assert "Canceled" in call_text

    # Shuold end conversation
    assert result == ConversationHandler.END


# --- /status ---

@patch('src.telegram_bot_handlers.get_location')
def test_status_command_with_location(mock_get_location):
    """Test /status – user has location."""
    mock_get_location.return_value = (52.23, 21.01, "Warszawa")

    mock_update = create_mock_update()
    mock_context = MagicMock()

    asyncio.run(status_command(mock_update, mock_context))

    call_text = mock_update.message.reply_text.call_args.args[0]
    assert "Warszawa" in call_text


@patch('src.telegram_bot_handlers.get_location')
def test_status_command_without_location(mock_get_location):
    """Test /status – user has no location."""
    mock_get_location.return_value = None

    mock_update = create_mock_update()
    mock_context = MagicMock()

    asyncio.run(status_command(mock_update, mock_context))

    call_text = mock_update.message.reply_text.call_args.args[0]
    assert "not been set" in call_text or "not set" in call_text


# --- create_bot_application ---

@patch('src.telegram_bot_handlers.create_tables')
@patch('src.telegram_bot_handlers.os.getenv')
def test_create_bot_application_no_token(mock_getenv, mock_create_tables):
    """Test creating app with no token."""
    mock_getenv.return_value = None

    with pytest.raises(ValueError, match="TELEGRAM_BOT_TOKEN"):
        create_bot_application()


@patch('src.telegram_bot_handlers.create_tables')
@patch('src.telegram_bot_handlers.Application')
@patch('src.telegram_bot_handlers.os.getenv')
def test_create_bot_application_success(mock_getenv, mock_application, mock_create_tables):
    """Test App building - success."""
    mock_getenv.return_value = "test_token_123"

    # Mock Application builder pattern
    mock_app = MagicMock()
    mock_builder = MagicMock()
    mock_builder.token.return_value = mock_builder
    mock_builder.build.return_value = mock_app
    mock_application.builder.return_value = mock_builder

    result = create_bot_application()

    # Check if  Application was created
    mock_application.builder.assert_called_once()
    mock_builder.token.assert_called_once_with("test_token_123")
    mock_builder.build.assert_called_once()

    # Check if tables were created
    mock_create_tables.assert_called_once()

    # Check result
    assert result == mock_app