import asyncio
import os
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_image_url(img_tag, base_url):
    if not img_tag:
        return "No image available"
    possible_attrs = ['data-src', 'data-original', 'data-lazy-src', 'src', 'data-srcset']
    for attr in possible_attrs:
        img_src = img_tag.get(attr)
        if img_src:
            if img_src.startswith("//"):
                return f"https:{img_src}"
            elif img_src.startswith("/"):
                return urljoin(base_url, img_src)
            elif img_src.startswith("http"):
                return img_src
    return "No image available"

def get_title(article):
    possible_tags = ['figcaption', 'span.title', 'h2', 'h3', 'h4']
    for tag in possible_tags:
        found = article.find_next(tag) or article.select_one(tag)
        if found and found.text.strip():
            return found.text.strip()
    return "No title available"

async def scrape_times_of_india_news():
    url = "https://timesofindia.indiatimes.com/"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })
        await page.goto(url, wait_until="domcontentloaded")
        for _ in range(3):
            await page.evaluate("window.scrollBy(0, document.body.scrollHeight / 3)")
            await page.wait_for_timeout(1000)
        html_content = await page.content()
        await browser.close()

        soup = BeautifulSoup(html_content, "html.parser")
        articles = soup.select("figure a")

        news = []
        for article in articles:
            link = urljoin(url, article.get('href', ''))
            img_tag = article.find("img") or article.parent.find("img")
            img_src = get_image_url(img_tag, url)
            title = get_title(article)

            if title != "No title available" and link and img_src != "No image available":
                news.append({
                    "title": title,
                    "link": link,
                    "image_url": img_src
                })

        # Insert into Supabase
        for item in news:
            supabase.table("news").insert(item).execute()

        print(f"Inserted {len(news)} news items into Supabase.")
        return news

if __name__ == "__main__":
    asyncio.run(scrape_times_of_india_news())
