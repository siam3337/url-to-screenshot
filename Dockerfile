FROM python:3.9-slim

# Install Chromium + dependencies
RUN apt-get update && apt-get install -y \
    chromium chromium-driver \
    fonts-liberation \
    libatk1.0-0 libatk-bridge2.0-0 libcups2 \
    libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 \
    libgbm1 libgtk-3-0 libnspr4 libnss3 libxcb1 \
    libxrandr2 libxshmfence1 libasound2 libpangocairo-1.0-0 \
    libx11-xcb1 libx11-6 libxext6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .

EXPOSE 10000

# Start Uvicorn on fixed port 10000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "10000"]
