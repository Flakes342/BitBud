import subprocess
import urllib.parse
import asyncio
from playwright.async_api import async_playwright
from selenium import webdriver
import time


async def _scrape_google_ai_answer(query):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        encoded_query = urllib.parse.quote_plus(query)
        search_url = f"https://www.google.com/search?q={encoded_query}"
        await page.goto(search_url, timeout=60000)
        await page.wait_for_timeout(5000)
        print ("I am here")

        # Try finding Gemini-style AI Overview summary
        try:
            selectors_to_try = [
                "div[data-attrid='wa:/description']",
                "div[jscontroller]",
                "div[data-md='139'] div span",  # fallback
                "div.xpdopen",
                "div[jsname='WbKHeb']",  # Often used for AI Overview
                "div[data-attrid='wa:/description']",  # Sometimes general summary
                "div[data-md='139']",
                "div[class*='AIanswer']",  # backup generic
                "div[jsname='K7J75c']",  # Gemini AI answer
                "div[jsname='C4z5Vb']",  # Gemini AI answer
                "div[jsname='C4z5Vb'] div[jsname='WbKHeb']",  # Gemini AI answer
                "div[jsname='WbKHeb'] div[jsname='C4z5Vb']",  # Gemini AI answer        
            ]

            for selector in selectors_to_try:
                box = await page.query_selector(selector)
                if box:
                    text = await box.inner_text()
                    if len(text.strip()) > 20:
                        await browser.close()
                        return text.strip()
            print ("No AI summary found.")
            return "No AI summary found."

        except Exception as e:
            return f"Error: {e}"
        finally:
            await browser.close()


def search_web(query):

    summary = asyncio.run(_scrape_google_ai_answer(query))
    if summary and summary!='No AI summary found.':
        return summary

    encoded_query = urllib.parse.quote_plus(query)
    url = f"https://www.google.com/search?q={encoded_query}"
    cmd = f"firefox {url}"
    subprocess.Popen(cmd, shell=True)
    return f"Searching for: {query}"
