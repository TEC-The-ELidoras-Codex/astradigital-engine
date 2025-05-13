FROM python:3.10-slim

LABEL maintainer="TEC - The Elidoras Codex"
LABEL description="Docker image for TEC AI agents and integrations"

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories if they don't exist
RUN mkdir -p config data logs

# Copy the rest of the application
COPY . .

# Port for Gradio app
EXPOSE 7860

# Environment setup
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Create empty .env file if it doesn't exist
RUN if [ ! -f config/.env ]; then touch config/.env; fi

# Command to run the application
CMD ["python", "app.py"]
