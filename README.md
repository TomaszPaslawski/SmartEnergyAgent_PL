# SmartEnergyAgent_PL
GitHub Workflow Status (placeholder)
Python 3.12
License: MIT
1. Project Overview

The Smart Energy Agent for Poland is an AI-powered system designed to assist users in optimizing their electricity consumption and energy storage management. It achieves this by providing timely and intelligent recommendations based on predicted electricity prices for the Polish market and localized weather forecasts.

This project aims to combine robust data fetching, analytical capabilities, and automated notifications into a single, reliable agent, demonstrating advanced skills in Data Engineering, Python development, and MLOps principles.

2. Key Features (Current & Planned)
```text
    Automated Data Collection:
        Electricity Prices: Daily fetching of hourly (15-minute intervals) electricity prices for the Polish Day-Ahead Market (RDN) from PSE Operator API.
        Weather Forecasts: Daily fetching of hourly weather forecasts (including cloud cover, temperature) for a specified location from Open-Meteo.com API.
    Intelligent Analysis:
        Identification of predicted high-price periods (morning and evening peaks).
        Evaluation of weather conditions to determine energy storage recharge potential (e.g., from solar PV).
    Personalized Recommendations: Generation of actionable advice for energy storage management (e.g., "discharge battery in the morning due to high prices, expect full recharge during the day").
    Automated Notifications: Delivery of recommendations via a Telegram bot.
    Robustness & Resilience: Incorporating MLOps practices for reliable operation.
```

3. Tech Stack

The project is built in Python and leverages a modern tech stack for efficiency and maintainability:
```text
    Programming Language: Python (currently 3.12)
    Project Management & Dependency Management: Poetry
    Data Fetching:
        requests (for PSE API communication)
        openmeteo-requests (dedicated client for Open-Meteo API)
        requests-cache & retry-requests (for resilient and efficient API calls)
    Data Processing & Analysis: Pandas
    Environment Variables: python-dotenv
    Scheduling: APScheduler (for automated daily runs)
    Notifications: python-telegram-bot
    Version Control: Git / GitHub
    Development Environment: PyCharm
```
4. Project Structure

The current and evolving directory structure of the project:

```text
.
├── .poetry/                    # Poetry configuration for in-project virtual environment
│   └── config.toml             # Local poetry configuration
├── src/                        # Source code for the agent's modules
│   ├── __init__.py             # Marks 'src' as a Python package
│   ├── agent_core.py           # Main logic to orchestrate data fetching and analysis
│   ├── data_fetcher.py         # Handles fetching electricity price data from PSE
│   ├── weather_fetcher.py      # Handles fetching weather forecast data from Open-Meteo
│   └── price_analyzer.py       # Placeholder for electricity price analysis logic
├── .cache/                     # Cache directory for API requests (managed by requests-cache)
├── .venv/                      # Poetry's virtual environment (if in-project is enabled)
├── .env                        # Environment variables (IGNORED by Git, local only)
├── .env.example                # Template for .env file
├── .gitignore                  # Files and directories ignored by Git
├── LICENSE                     # MIT License
├── README.md                   # This file
├── pyproject.toml              # Project metadata and Poetry dependencies
└── poetry.lock                 # Lock file for deterministic dependency management
```
5. Setup & Installation

To set up and run the project locally, follow these steps:

   Clone the Repository:

  ```Bash
  git clone https://github.com/YourGitHubUsername/SmartEnergyAgent_PL.git
  cd SmartEnergyAgent_PL
  ```
  Install Poetry:

  If you don't have Poetry installed globally, follow the official instructions: Poetry Installation Guide
  Configure Poetry for In-Project Virtual Environment:

  ```Bash
    poetry config virtualenvs.in-project true --local
  ```

  Install Project Dependencies:

  ```Bash

    poetry install --no-root # --no-root is important if you haven't run poetry init
  ```
  (This will create the
    .venv and install all packages listed in pyproject.toml and poetry.lock).
    Configure PyCharm:
        Open the project in PyCharm.
        Go to File > Settings > Project: SmartEnergyAgent_PL > Python Interpreter.
        Click the gear icon, select Add New Interpreter..., choose Poetry Environment, and select Use existing environment. PyCharm should autodetect the .venv created by Poetry.
    Create .env file:
        Create a file named .env in the project root.
        Add your API keys and base URLs (e.g., PSE_API_BASE_URL, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID) following the structure of .env.example.

  ```dotenv
    # .env example
    PSE_API_BASE_URL="https://api.raporty.pse.pl/api/rce-pln"
    # TELEGRAM_BOT_TOKEN="your_telegram_bot_token"
    # TELEGRAM_CHAT_ID="your_telegram_chat_id"
```

6. Usage

    Run the agent logic:

    ```Bash
    poetry run python src/agent_core.py
    ```

    (Note: The agent includes a check for PSE price publication time (after 14:00 CET/CEST). If run before this time for next-day data, it will exit with a warning.)

7. MLOps / DataOps Practices

This project is developed with MLOps and DataOps principles from the outset:

```text
    Version Control for Code & Dependencies: Git for code, Poetry (pyproject.toml, poetry.lock) for deterministic dependency management.
    Modular Design: Code is structured into distinct, reusable modules (data_fetcher, weather_fetcher, price_analyzer).
    Environment Management: Isolated virtual environments using Poetry.
    Secure Configuration: Use of .env and python-dotenv for sensitive information.
    Resilient API Calls: requests-cache and retry-requests ensure robust data fetching.
    Automated Scheduling (Planned): APScheduler for reliable daily execution.
```

8. Roadmap

```text

    Phase 1: Setup & Data Fetching (COMPLETE): Project initialization, Poetry setup, PSE electricity price fetching, Open-Meteo weather forecast fetching.
    Phase 2: Data Analysis: Implement price peak detection, weather recharge potential assessment.
    Phase 3: Recommendation Engine: Develop logic to combine price and weather analysis into actionable advice.
    Phase 4: Notification System: Implement Telegram bot integration.
    Phase 5: Orchestration & Deployment: Use APScheduler for automation, explore Docker for deployment.
```

10. License

This project is licensed under the MIT License. See the LICENSE file for more details.

10. Contact

Tomasz Pasławski
https://github.com/TomaszPaslawski

