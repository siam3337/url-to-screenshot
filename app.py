from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, JSONResponse
from pyppeteer import launch
import uuid
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("screenshot-api")

app = FastAPI()
OUTPUT_DIR = "screenshots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Health check endpoint — responds immediately
@app.get("/")
def home():
    return {"message": "Screenshot API is running"}

# Screenshot endpoint — launches Chromium on-demand
@app.get("/screenshot")
async def screenshot(url: str = Query(...), full_page: bool = False):
    filename = f"{uuid.uuid4().hex}.png"
    filepath = os.path.join(OUTPUT_DIR, filename)
    try:
        logger.info(f"Launching Chromium for {url}")
        browser = await launch(
            executablePath="/usr/bin/chromium",
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
        await page.screenshot({"path": filepath, "fullPage": full_page})
        await browser.close()
        return FileResponse(filepath, media_type="image/png", filename=filename)
    except Exception as e:
        logger.error(f"Screenshot error: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)
