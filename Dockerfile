FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Fix any broken dpkg state
RUN dpkg --configure -a

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 python3-pip python3-venv \
        gcc \
        sox \
        ffmpeg \
        git \
        openssh-server \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -u 10014 -m -s /bin/bash appuser

# Set up workdir and copy files
WORKDIR /app
COPY . /app

# Install Python dependencies
RUN pip3 install --upgrade pip && pip3 install --no-cache-dir -r requirements.txt

# Set permissions
RUN chown -R 10014:0 /app

USER 10014

# (Optional) Expose port if you need it, e.g. for Flask
EXPOSE 8080

# Default command (change as needed)
CMD ["python3", "app.py"]