# Use the slim version of the Python image
FROM python:3.10-slim

# Set environment variables for Poetry
ENV POETRY_VERSION=1.8.0
ENV PATH="/root/.local/bin:$PATH"

# Expose the default HTTP port
EXPOSE 8501

# Set the working directory
WORKDIR /app

# Install system dependencies for Poetry and Streamlit
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry==${POETRY_VERSION}

# Copy only the dependency files first
COPY pyproject.toml poetry.lock /app/

# Install the dependencies using Poetry
RUN poetry install --no-dev --no-interaction --no-ansi

# Copy the rest of the application code
COPY . .

# Command to run your Streamlit app on port 80
CMD ["poetry", "run", "streamlit", "run", "--server.port", "8501", "weather_app/weather.py"]