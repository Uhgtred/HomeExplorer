FROM ubuntu:22.04
LABEL authors="Markus"

# Install python and pip
RUN apt update --allow-releaseinfo-change && \
    apt install -y --no-install-recommends python3 python3-pip python3-venv ffmpeg libsm6 libxext6 libgl1-mesa-glx && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements to app-folder
COPY requirements.txt /app/
WORKDIR /app/

# open specified port to the outside
ENV PORT=2000
EXPOSE 2000

# Install dependencies
RUN python3 -m venv /app/venv && \
    /app/venv/bin/pip3 install --upgrade pip && \
    /app/venv/bin/pip3 install -r /app/requirements.txt

# Copy SourceCode to app-folder
COPY ../ /app/

## set environment for python-version
ENV PATH="/app/venv/bin:${PATH}"