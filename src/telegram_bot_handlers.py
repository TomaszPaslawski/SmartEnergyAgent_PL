import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)
from src.location_service import geocode_city, validate_coordinates
from src.database import create_tables, save_location, get_location
from src.data_fetcher import get_electricity_prices_pse
from src.weather_fetcher import get_weather_forecast
from src.price_analyzer import analyze_price_peaks
from src.weather_analyzer import analyze_weather_for_recharge
from src.recommendation_engine import generate_recommendations
from datetime import datetime, timedelta
import pytz

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Conversation status
WAITING_FOR_CITY = 1


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handler for command /start.
    Welcomes user and ask for location.
    """
    user_id = str(update.effective_user.id)
    user_name = update.effective_user.first_name or "User"

    # Check if user has already location
    existing_location = get_location(user_id)

    if existing_location:
        lat, lon, city = existing_location
        await update.message.reply_text(
            f"Welcome again, {user_name}!\n\n"
            f"Your current location is: <b>{city}</b>\n"
            f"   ({lat:.2f}°N, {lon:.2f}°E)\n\n"
            f"To change location use: /set_location",
            parse_mode='HTML'
        )
        return ConversationHandler.END
    else:
        await update.message.reply_text(
            f"Welcome, {user_name}!\n\n"
            f"I am SmartEnergyAgent – I help to reduce energy costs.\n\n"
            f"Please set your location.\n"
            f"Enter your's city name (e.g. <b>Warszawa</b>, <b>Kraków</b>, <b>Gdańsk</b>):",
            parse_mode='HTML'
        )
        return WAITING_FOR_CITY


async def set_location_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handler for command /set_location.
    Starts process of setting the location.
    """
    await update.message.reply_text(
        "Please provide new location.\n"
        "Enter city name (e.g. <b>Warszawa</b>, <b>Kraków</b>, <b>Gdańsk</b>):",
        parse_mode='HTML'
    )
    return WAITING_FOR_CITY


async def receive_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handler to take city name from user.
    Makes geocoding and saves location.
    """
    user_id = str(update.effective_user.id)
    city_name = update.message.text.strip()

    # Inform user about seeking for location
    await update.message.reply_text(f"Searching: <b>{city_name}</b>...", parse_mode='HTML')

    # Geocoding
    result = geocode_city(city_name)

    if result is None:
        await update.message.reply_text(
            f"Location not found: <b>{city_name}</b>\n\n"
            f"Please try again - enter city name:",
            parse_mode='HTML'
        )
        return WAITING_FOR_CITY

    lat, lon, display_name = result

    # Coordinates validation
    if not validate_coordinates(lat, lon):
        await update.message.reply_text(
            f"Incorrect coordinates for: <b>{city_name}</b>\n\n"
            f"Please try again - enter city name:",
            parse_mode='HTML'
        )
        return WAITING_FOR_CITY

    # Save in the database
    success = save_location(user_id, lat, lon, city_name)

    if success:
        await update.message.reply_text(
            f"Location saved!\n\n"
            f" <b>{display_name}</b>\n"
            f"   ({lat:.2f}°N, {lon:.2f}°E)\n\n"
            f"Starting from tomorrow at 14:00 You will receive daily recommendations .\n\n"
            f"Options:\n"
            f"/set_location – change location\n"
            f"/status – check current location\n",
            parse_mode='HTML'
        )
    else:
        await update.message.reply_text(
            "Error occured during location saving. Please try again later."
        )

    return ConversationHandler.END


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handler for command /cancel.
    Cancels location setting.
    """
    await update.message.reply_text("Canceled. You can return using command /set_location")
    return ConversationHandler.END


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handler for command /status.
    Shows actual user's location.
    """
    user_id = str(update.effective_user.id)
    location = get_location(user_id)

    if location:
        lat, lon, city = location
        await update.message.reply_text(
            f"Current location: <b>{city}</b>\n"
            f"   ({lat:.2f}°N, {lon:.2f}°E)\n\n"
            f"Recommendations send daily at 14:00 CET/CEST\n\n"
            f"For change: /set_location",
            parse_mode='HTML'
        )
    else:
        await update.message.reply_text(
            "Location has not been set yet.\n\n"
            "Use: /start or: /set_location to set location."
        )


async def recommend_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handler for /recommend command.
    Generates and sends recommendations on demand.
    """
    user_id = str(update.effective_user.id)
    poland_tz = pytz.timezone('Europe/Warsaw')

    # Check if user has location
    location = get_location(user_id)

    if not location:
        await update.message.reply_text(
            "You don't have a location set.\n\n"
            "Use /start or /set_location first."
        )
        return

    latitude, longitude, city_name = location

    # Calculate target date (tomorrow)
    current_time = datetime.now(poland_tz)
    target_date = (current_time + timedelta(days=1)).date()

    await update.message.reply_text(
        f"Generating recommendations for <b>{city_name}</b>...\n"
        f"Date: {target_date.strftime('%Y-%m-%d')}",
        parse_mode='HTML'
    )

    try:
        # 1. Fetch electricity prices
        prices_df = get_electricity_prices_pse(target_date.strftime('%Y-%m-%d'))
        if prices_df is None or prices_df.empty:
            await update.message.reply_text(
                "PSE price data is not available yet.\n"
                "Try again later (PSE publishes data between 13:00-14:00 CET)."
            )
            return

        # 2. Analyze prices
        price_analysis = analyze_price_peaks(prices_df)

        # 3. Fetch weather
        weather_df = get_weather_forecast(latitude, longitude, target_date.strftime('%Y-%m-%d'))
        if weather_df is None or weather_df.empty:
            await update.message.reply_text(
                "Weather forecast is not available.\n"
                "Try again later."
            )
            return

        # 4. Analyze weather
        weather_analysis = analyze_weather_for_recharge(weather_df)

        # 5. Generate recommendations
        recommendation = generate_recommendations(price_analysis, weather_analysis, target_date)

        # 6. Send recommendation
        await update.message.reply_text(recommendation, parse_mode='HTML')

    except Exception as e:
        logger.error(f"Error generating recommendations for user {user_id}: {e}")
        await update.message.reply_text(
            "An error occurred while generating recommendations.\n"
            "Please try again later."
        )

def create_bot_application() -> Application:
    """
    Creates and configures Telegram Bot Application.

    Returns:
        Application: Telegram Bot Configured.
    """
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not bot_token:
        logger.error("TELEGRAM_BOT_TOKEN not found!")
        raise ValueError("TELEGRAM_BOT_TOKEN not set")

    # Creating application
    application = Application.builder().token(bot_token).build()

    # Conversation handler (start → wait for city)
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start_command),
            CommandHandler("set_location", set_location_command),
        ],
        states={
            WAITING_FOR_CITY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_city),
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel_command),
        ],
    )

    # Handlers registration
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("recommend", recommend_command))

    # Creates tables in database
    create_tables()

    logger.info("Telegram Bot application created successfully.")
    return application