# This tells Docker to use Python 3.11 as the base
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# These environment variables optimize Python for containers
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=main.py \
    FLASK_ENV=production

# Install system dependencies (needed for some Python packages)
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt first (this helps with Docker caching)
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy all your application files
COPY . .

# Create directory for the database
RUN mkdir -p /app/instance && chmod 755 /app/instance

# Tell Docker this container listens on port 5000
EXPOSE 5000

# Create a non-root user for security
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

# Command to run when container starts
CMD ["python", "main.py"]