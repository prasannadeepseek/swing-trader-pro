# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY . .

RUN apt-get update && \
    apt-get install -y build-essential && \
    pip install -r requirements.txt && \
    apt-get remove -y build-essential && \
    apt-get autoremove -y

CMD ["python", "main.py"]

# version 2
# syntax=docker/dockerfile:1

FROM python:3.9-slim

# Set environment variables for Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

WORKDIR /app

# Install build dependencies, then remove them after pip install
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copy only requirements first for better cache
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the code
COPY . .

# Create a non-root user and switch to it
RUN useradd -m appuser && \
    chown -R appuser /app
USER appuser

# (Optional) EXPOSE if your app serves HTTP
# EXPOSE 8000

CMD ["python", "main.py"]