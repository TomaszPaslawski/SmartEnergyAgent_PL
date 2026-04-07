# SmartEnergyAgent_PL

![Tests](https://github.com/TomaszPaslawski/SmartEnergyAgent_PL/workflows/Tests/badge.svg)
![Coverage](https://img.shields.io/badge/coverage-99%25-brightgreen)
![Python](https://img.shields.io/badge/python-3.12-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Deployment](https://img.shields.io/badge/deployment-Railway-purple)

## 1. Project Overview

**Smart Energy Agent for Poland** is an AI-powered system that helps users optimize electricity consumption and energy storage management. It provides daily intelligent recommendations based on:

- **Day-ahead electricity prices** from the Polish PSE market
- **Localized weather forecasts** for solar PV potential assessment
- **Price peak analysis** (morning & evening peaks, low/negative prices)
- **Weather analysis** for battery recharge conditions

The agent runs **24/7 in the cloud** (Railway), sends **daily Telegram notifications** at 14:00 CET/CEST, and supports **multiple users** with personalized locations.

## 2. Key Features

### ✅ Implemented

- **Automated Data Collection:**
  - Electricity prices (15-min intervals) from PSE Operator API
  - Hourly weather forecasts from Open-Meteo API (ECMWF model)

- **Intelligent Analysis:**
  - Identification of 6 highest and 3 lowest price hours
  - Price threshold monitoring (500 PLN/MWh)
  - Weather evaluation for PV recharge potential (cloud cover, weather codes)

- **Personalized Recommendations:**
  - Morning/evening peak price alerts
  - Battery charge/discharge timing recommendations
  - Low/negative price opportunity alerts
  - Surplus energy selling recommendations

- **Telegram Bot:**
  - `/start` – Welcome & set location
  - `/set_location` – Change location (geocoding: city name → coordinates)
  - `/status` – Show current location
  - `/recommend` – Generate recommendations on demand
  - Automated daily notifications at 14:00 CET/CEST

- **Multi-User Support:**
  - SQLite database for user locations
  - Each user receives personalized recommendations
  - Geocoding via Nominatim API (OpenStreetMap)

- **Cloud Deployment:**
  - Railway.app (24/7 operation)
  - Docker containerization
  - Environment variables for secrets management

- **CI/CD:**
  - GitHub Actions – automated tests on every push
  - 80+ tests with ~99% average code coverage

- **MLOps/DataOps Practices:**
  - Poetry for dependency management
  - Modular architecture (10 modules)
  - Comprehensive error handling and logging
  - Timezone-aware scheduling (Europe/Warsaw)

## 3. Architecture

```text
┌─────────────────────────────────────────────┐
│              Railway (Cloud)                  │
│                                              │
│  ┌─────────────┐    ┌──────────────────┐    │
│  │  Scheduler   │    │  Telegram Bot    │    │
│  │  (14:00 CET) │    │  (24/7 polling)  │    │
│  └──────┬───────┘    └────────┬─────────┘    │
│         │                     │              │
│         ▼                     ▼              │
│  ┌─────────────────────────────────────┐    │
│  │         agent_core.py               │    │
│  │    (orchestration layer)            │    │
│  └──────┬──────────────────┬───────────┘    │
│         │                  │                │
│    ┌────▼────┐      ┌─────▼──────┐         │
│    │  Data    │      │  Weather    │         │
│    │ Fetcher  │      │  Fetcher   │         │
│    │ (PSE API)│      │(Open-Meteo)│         │
│    └────┬─────┘      └─────┬──────┘         │
│         │                  │                │
│    ┌────▼────┐      ┌─────▼──────┐         │
│    │  Price   │      │  Weather    │         │
│    │ Analyzer │      │  Analyzer  │         │
│    └────┬─────┘      └─────┬──────┘         │
│         │                  │                │
│         ▼                  ▼                │
│  ┌─────────────────────────────────────┐    │
│  │     Recommendation Engine           │    │
│  └──────────────┬──────────────────────┘    │
│                 │                           │
│          ┌──────▼──────┐                    │
│          │  Telegram    │                    │
│          │ Notification │                    │
│          └─────────────┘                    │
│                                              │
│  ┌──────────────┐  ┌───────────────────┐    │
│  │   SQLite DB   │  │ Location Service  │    │
│  │(user locations)│  │  (Nominatim API) │    │
│  └──────────────┘  └───────────────────┘    │
└─────────────────────────────────────────────┘
```

## 4. Tech Stack

|       Category        |                    	Technology                     |
|:---------------------:|:--------------------------------------------------:|
|       Language        |                    	Python 3.12                    |
| Dependency Management |                      	Poetry                       |
|    Data Processing    |                   	Pandas, NumPy                   |
|         APIs          | 	PSE Operator, Open-Meteo, Nominatim, Telegram Bot |
|       Database        |                      	SQLite                       |
|      Scheduling       |                    	APScheduler                    |
|     Notifications     |                	python-telegram-bot                |
|      Deployment       |                	Docker, Railway.app                |
|         CI/CD         |                  	GitHub Actions                   |
|        Testing        |         	pytest, pytest-cov, unittest.mock         |
|    Version Control    |                   	Git / GitHub                    |
|          IDE          |                      	PyCharm                      |
## 5. Project Structure

```text

.
├── .github/
│   └── workflows/
│       └── tests.yml              # CI/CD: automated testing
├── src/
│   ├── __init__.py
│   ├── agent_core.py              # Main orchestration + scheduler
│   ├── data_fetcher.py            # PSE electricity price fetching
│   ├── weather_fetcher.py         # Open-Meteo weather forecast fetching
│   ├── price_analyzer.py          # Electricity price analysis
│   ├── weather_analyzer.py        # Weather analysis for PV recharge
│   ├── recommendation_engine.py   # Recommendation generation
│   ├── notification_manager.py    # Telegram message sending
│   ├── location_service.py        # Geocoding (city → coordinates)
│   ├── database.py                # SQLite database operations
│   └── telegram_bot_handlers.py   # Telegram bot commands
├── tests/
│   ├── test_data_fetcher.py       # Tests for data_fetcher (100% coverage)
│   ├── test_weather_fetcher.py    # Tests for weather_fetcher (100% coverage)
│   ├── test_price_analyzer.py     # Tests for price_analyzer (96% coverage)
│   ├── test_weather_analyzer.py   # Tests for weather_analyzer (97% coverage)
│   ├── test_recommendation_engine.py  # Tests for recommendations (100% coverage)
│   ├── test_notification_manager.py   # Tests for notifications (100% coverage)
│   ├── test_agent_core.py         # Tests for agent_core (96% coverage)
│   ├── test_location_service.py   # Tests for location_service (100% coverage)
│   ├── test_database.py           # Tests for database (100% coverage)
│   └── test_telegram_bot_handlers.py  # Tests for bot handlers (100% coverage)
├── data/                          # SQLite database (gitignored)
├── Dockerfile                     # Docker configuration
├── Procfile                       # Railway deployment
├── requirements.txt               # Python dependencies (for Railway)
├── pyproject.toml                 # Poetry configuration
├── poetry.lock                    # Dependency lock file
├── .env                           # Environment variables (gitignored)
├── .env.example                   # Environment variables template
├── .gitignore
├── LICENSE                        # MIT License
└── README.md                      # This file
```

## 6. Test Coverage

|          Module          |   	Tests    | 	Coverage |
|:------------------------:|:-----------:|:---------:|
|     data_fetcher.py      |     	✅      |   	100%   |
|    weather_fetcher.py    |     	✅	     |   100%    |
|    price_analyzer.py     | 	✅ 6 tests  |   	96%    |
|   weather_analyzer.py    | 	✅ 19 tests |   	97%    |
| recommendation_engine.py | 	✅ 7 tests  |   	100%   |
| notification_manager.py  | 	✅ 6 tests  |   	100%   |
|      agent_core.py       | 	✅ 4 tests  |   	96%    |
|   location_service.py    | 	✅ 8 tests  |   	100%   |
|       database.py        | 	✅ 12 tests |   	100%   |
| telegram_bot_handlers.py | 	✅ 12 tests |   	100%   |
|          Total           | 	80+ tests  | 	~99% avg |

## 7. Setup & Installation

### Prerequisites

**Python 3.12+**

**Poetry (installation guide)**

**Telegram Bot Token (BotFather)**

### Local Development

```Bash

# Clone repository
git clone https://github.com/TomaszPaslawski/SmartEnergyAgent_PL.git
cd SmartEnergyAgent_PL

# Install dependencies
poetry install

# Create .env file
cp .env.example .env
# Edit .env with your credentials:
# TELEGRAM_BOT_TOKEN=your_token
# TELEGRAM_CHAT_ID=your_chat_id

# Run tests
poetry run pytest tests/ -v --cov=src

# Run agent locally
poetry run python src/agent_core.py
```

### Docker

```Bash

# Build image
docker build -t smartenergyagent .

# Run container
docker run -e TELEGRAM_BOT_TOKEN=your_token -e TELEGRAM_CHAT_ID=your_chat_id smartenergyagent
```

### Railway Deployment

**Fork/clone this repository**

**Connect to Railway.app**

**Deploy from GitHub**

**Set environment variables:**

  - TELEGRAM_BOT_TOKEN

  - TELEGRAM_CHAT_ID

**Agent runs 24/7 automatically**

## 8. Telegram Bot Commands

|Command|Description|
| :--- | :--- |
|/start|	Welcome message + set location|
|/set_location|	Change your location (enter city name)|
|/status|	Show your current location|
|/recommend|	Generate recommendations on demand|
|/cancel|	Cancel current operation|

Example Interaction

```text

User: /start
Bot:  👋 Welcome! Enter your city name:

User: Warszawa
Bot:  🔍 Searching: Warszawa...
      ✅ Location saved!
      📍 Warszawa, województwo mazowieckie, Polska
      (52.23°N, 21.01°E)

      🔋 You will receive daily recommendations at 14:00 CET/CEST.

User: /recommend
Bot:  🔄 Generating recommendations for Warszawa...
      📊 Recommendations for 2026-03-14:
      1. Weather favorable for PV charging: YES
      2. Morning peak: 07:00 (600.00 PLN/MWh)
      3. No negative prices during PV hours
      4. Recommended charging start: 10:00
      5. Recommended discharge: 07:00
      6. Evening peak: 17:00 (650.00 PLN/MWh)
      ...
  ```

## 9. MLOps / DataOps Practices

**Version Control:** Git for code, Poetry for dependencies

**CI/CD:** GitHub Actions – automated testing on every push

**Testing:** 80+ tests, ~99% coverage, mocking external APIs

**Containerization:** Docker for reproducible deployments

**Cloud Deployment:** Railway.app (24/7 operation)

**Database:** SQLite for user data persistence

**Error Handling:** Comprehensive try/except with logging

**Timezone Awareness:** Europe/Warsaw (CET/CEST)

**Secrets Management:** Environment variables (not in code)

**Modular Architecture:** 10 independent, testable modules

## 10. Roadmap

**✅ Phase 1: Data Fetching (PSE + Open-Meteo)**

**✅ Phase 2: Price & Weather Analysis**

**✅ Phase 3: Recommendation Engine**

**✅ Phase 4: Telegram Notifications**

**✅ Phase 5: Cloud Deployment (Railway + Docker)**

**✅ Phase 6: CI/CD (GitHub Actions)**

**✅ Phase 7: Multi-User Support (SQLite + Geocoding)**

**✅ Phase 8: Telegram Bot Commands (/start, /set_location, /recommend)**

Phase 9: Historical data tracking & trends

Phase 10: Web dashboard (Streamlit/Gradio)

Phase 11: Advanced ML predictions

Phase 12: PostgreSQL migration (scalability)

## 11. License

#### This project is licensed under the MIT License. See the LICENSE file for details.

## 12. Contact

#### Tomasz Pasławski

    GitHub: TomaszPaslawski
