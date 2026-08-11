FROM python:3.11-slim

# Prevent Python from buffering logs (important for Celery)

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

# Install system dependencies
RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip first to resolve dependencies correctly
RUN pip install --upgrade pip setuptools wheel

# Create a non-root user with the same UID/GID as your host
RUN groupadd -g 1000 appuser \
    && useradd -m -u 1000 -g appuser appuser

# Create directories and give ownership
RUN mkdir -p /code/logs /code/static \
    && chown -R appuser:appuser /code



# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Copy entrypoint
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Switch to the non-root user
USER appuser

ENTRYPOINT ["/entrypoint.sh"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]