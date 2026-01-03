# Use Python 3.10 slim
FROM python:3.10-slim

# Install system dependencies needed for OpenCV and DeepFace
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
 && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Ensure uploads directory exists
RUN mkdir -p uploads

# Start FastAPI using Railway's $PORT environment variable
CMD ["uvicorn", "face_server:app", "--host", "0.0.0.0", "--port", "${PORT}"]
