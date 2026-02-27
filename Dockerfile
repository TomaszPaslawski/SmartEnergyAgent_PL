# Base Python image
FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Copy ENTIRE project first (including src/)
COPY . .

# Install Poetry package manager
RUN pip install --no-cache-dir poetry

# Install project dependencies (production only, no dev packages)
RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi

# Environment variables for Telegram credentials
ENV TELEGRAM_BOT_TOKEN=""
ENV TELEGRAM_CHAT_ID=""

# Run the agent (scheduler starts automatically)
CMD ["python", "src/agent_core.py"]