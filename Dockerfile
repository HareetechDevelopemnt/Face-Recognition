FROM python:3.10-slim

# System dependencies (VERY IMPORTANT)
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies first (cache friendly)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Railway / Render compatible
CMD ["sh", "-c", "uvicorn face_server:app --host 0.0.0.0 --port ${PORT:-8000}"]
