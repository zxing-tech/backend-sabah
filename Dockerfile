# Use Python 3.11 (more stable with LiveKit than 3.14)
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY agent.py .
COPY customer_service2_resized.jpg .

# Expose port (LiveKit agents typically don't need exposed ports, but good practice)
EXPOSE 8080

# Run the agent in production mode
CMD ["python", "agent.py", "start"]
