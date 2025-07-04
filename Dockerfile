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

# Set up SSH
RUN mkdir /var/run/sshd
# Create a non-root user with home and bash shell, set password
RUN useradd -u 10014 -m -s /bin/bash appuser && echo 'appuser:appuser' | chpasswd
# Allow appuser SSH login, disable root login for security
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config
RUN sed -i 's@session\\s*required\\s*pam_loginuid.so@session optional pam_loginuid.so@g' /etc/pam.d/sshd
RUN echo 'AllowUsers appuser' >> /etc/ssh/sshd_config
ENV NOTVISIBLE="in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

# Set workdir
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy script
COPY generate_audio.py ./

# Show username and container IP on login for appuser
RUN echo 'echo "Username: $(whoami)"' >> /home/appuser/.bashrc
RUN echo 'echo "Container IP: $(hostname -I)"' >> /home/appuser/.bashrc


# Switch to non-root user
USER 10014

# Expose SSH port (can be after USER, no problem)
EXPOSE 22

# Start SSH server by default
CMD ["/usr/sbin/sshd", "-D"]
