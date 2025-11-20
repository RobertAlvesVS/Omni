from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from playwright.sync_api import sync_playwright  # ← sync, não async
import asyncio
from concurrent.futures import ThreadPoolExecutor

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Função que roda em thread separada
def executar_playwright_sync():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://playwright.dev")
        title = page.title()
        browser.close()
        return title

@app.get("/browser")
async def get_browser_title():
    # Roda Playwright em thread separada
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as pool:
        title = await loop.run_in_executor(pool, executar_playwright_sync)
    
    return {"title": title}