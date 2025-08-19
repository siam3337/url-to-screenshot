import asyncio
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from pyppeteer import launch
import uuid
import os
import subprocess

# Start helper.py
subprocess.Popen(["python", "helper.py"])

app = FastAPI()

OUTPUT_DIR = "screenshots"
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.get("/")
async def home():
    return {"message": "Screenshot API is running"}


@app.get("/screenshot")
async def screenshot(url: str = Query(..., description="Website URL"),
                     full_page: bool = False):
    """
    Generate a screenshot of the given URL using system Chromium.
    Example: /screenshot?url=https://example.com&full_page=true
    """
    filename = f"{uuid.uuid4().hex}.png"
    filepath = os.path.join(OUTPUT_DIR, filename)

    browser = await launch(
        executablePath="/usr/bin/chromium",   # Use system Chromium
        headless=True,
        args=[
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu"
        ]
    )
    page = await browser.newPage()
    await page.setViewport({"width": 1280, "height": 800})
    await page.goto(url, {"waitUntil": "networkidle2", "timeout": 60000})
    await page.screenshot({'path': filepath, 'fullPage': full_page})
    await browser.close()

    return FileResponse(filepath, media_type="image/png", filename=filename)
