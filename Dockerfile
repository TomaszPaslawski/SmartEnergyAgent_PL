# Base Python image
FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Copy dependency files first (for Docker layer caching)
COPY pyproject.toml poetry.lock ./

# Install Poetry package manager
RUN pip install --no-cache-dir poetry

# Install project dependencies (production only, no dev packages)
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Copy entire project into container
COPY . .

# Environment variables for Telegram credentials
# These will be set in Fly.io secrets (not hardcoded here)
ENV TELEGRAM_BOT_TOKEN=""
ENV TELEGRAM_CHAT_ID=""

# Run the agent (scheduler starts automatically)
CMD ["python", "src/agent_core.py"]