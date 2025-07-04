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
RUN echo 'root:root' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' /etc/pam.d/sshd
ENV NOTVISIBLE="in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

# Set workdir
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy script
COPY generate_audio.py ./

# Show username and container IP on login
RUN echo 'echo "Username: $(whoami)"' >> /root/.bashrc
RUN echo 'echo "Container IP: $(hostname -I)"' >> /root/.bashrc

# Expose SSH port
EXPOSE 22

# Start SSH server by default
CMD ["/usr/sbin/sshd", "-D"]
