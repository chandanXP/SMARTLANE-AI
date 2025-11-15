FROM python:3.10-slim

# ------------------------------------------------
# Install system packages required by OpenCV & YOLO
# ------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgl1 \
    libopencv-dev \
    python3-opencv \
    && rm -rf /var/lib/apt/lists/*

# ------------------------------------------------
# App directory
# ------------------------------------------------
WORKDIR /app

# ------------------------------------------------
# Install Python deps
# ------------------------------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ------------------------------------------------
# Copy all files
# ------------------------------------------------
COPY . .

# ------------------------------------------------
# Streamlit settings
# ------------------------------------------------
EXPOSE 7860
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_PORT=7860
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

CMD ["streamlit", "run", "app.py"]
