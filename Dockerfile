FROM ubuntu:22.04
LABEL authors="Markus"

# Install system dependencies
RUN apt update --allow-releaseinfo-change && \
    apt install -y --no-install-recommends \
        curl \
        ca-certificates \
        ffmpeg \
        libsm6 \
        libxext6 \
        libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# Create app directory
WORKDIR /app

# Copy project metadata first (for caching)
COPY pyproject.toml uv.lock* ./

# Create virtual environment using uv
RUN uv venv /app/venv

# Add venv to PATH
ENV PATH="/app/venv/bin:${PATH}"

# Install dependencies into the venv
RUN uv sync --frozen

# Copy the rest of the source code
COPY . .

# Expose port
ENV PORT=2000
EXPOSE 2000

# Run your app using uv
#CMD ["uv", "run", "main.py"]
