# Use official Python image as base
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        openssh-server \
        sox \
        ffmpeg \
        git \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy script
COPY generate_audio.py ./

# Create a non-root user and switch to it
RUN useradd -u 10014 -m -s /bin/bash appuser
USER 10014
