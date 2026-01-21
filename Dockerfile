# Mobile Resume Generator - Docker Image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for PDF generation
RUN apt-get update && apt-get install -y \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create output directory
RUN mkdir -p /app/output /app/data

# Expose port
EXPOSE 8080

# Environment variables (set these when running)
ENV CEREBRAS_API_KEY=""
ENV GROQ_API_KEY=""
ENV OPENROUTER_API_KEY=""
ENV PORT=8080

# Run with gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--timeout", "120", "app:app"]

