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

# Avoid Pyppeteer downloading its own Chromium
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=1
ENV PYPPETEER_CHROMIUM_EXECUTABLE=/usr/bin/chromium

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py screenshot_service.py .

EXPOSE 10000
EXPOSE 8000

# Start Flask (health check) + FastAPI runs in background
CMD ["python", "app.py"]
