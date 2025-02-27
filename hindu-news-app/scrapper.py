import requests
from bs4 import BeautifulSoup
import random
import time

def scrape_times_of_india_news():
    url = "https://timesofindia.indiatimes.com/"
    
    # Add headers to mimic a browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error: Status code {response.status_code}")
        return []
        
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Try multiple selector approaches
    articles = []
    
    # Method 1: Direct figure > a selector
    articles = soup.select("figure a")
    
    # If that doesn't yield enough results, try another approach
    if len(articles) < 5:
        print("Using fallback selector method")
        # Try to find articles by class patterns common in news sites
        articles = soup.select(".top-newslist .news-card, .lead-story a, .featured-news a")
    
    # Extract title, link, and image for each headline
    news = []
    for article in articles:
        # Try various ways to extract image
        img_tag = article.find("img")
        if not img_tag:
            img_tag = article.select_one("img") or article.parent.select_one("img")
        
        # Find title - try multiple approaches
        title_tag = article.find_next("figcaption")
        if not title_tag or not title_tag.text.strip():
            title_tag = article.select_one("span.title, h2, h3") or article.find("span", class_="title")
            if not title_tag:
                # Try to find nearby heading
                for heading in ['h2', 'h3', 'h4']:
                    title_tag = article.parent.find(heading)
                    if title_tag:
                        break
        
        # Extract link
        link = article.get('href', "No link available")
        if link != "No link available" and not link.startswith("https"):
            link = f"{url.rstrip('/')}{link}"
        
        # Extract image source
        img_src = "No image available"
        if img_tag:
            # Try multiple image attributes
            for attr in ['data-src', 'src', 'data-original', 'data-lazy-src']:
                if img_tag.get(attr):
                    img_src = img_tag[attr]
                    if not img_src.startswith("http"):
                        img_src = f"https:{img_src}" if img_src.startswith("//") else f"{url.rstrip('/')}{img_src}"
                    break
        
        # Extract title text
        title = title_tag.text.strip() if title_tag else "No title available"
        
        # Skip duplicates and incomplete entries
        if title != "No title available" and link != "No link available" and not any(item['title'] == title for item in news):
            news.append({"title": title, "link": link, "image": img_src})
    
    # Add debug info
    with open("debug_info.txt", "w", encoding="utf-8") as debug_file:
        debug_file.write(f"Status code: {response.status_code}\n")
        debug_file.write(f"Content length: {len(response.content)}\n")
        debug_file.write(f"Articles found: {len(articles)}\n")
        debug_file.write(f"News items extracted: {len(news)}\n")
    
    # Save data to file
    with open("news_data.txt", "w", encoding="utf-8") as file:
        for item in news:
            file.write(f"{item['title']} - {item['link']} - {item['image']}\n")
    
    print(f"Scraped {len(news)} headlines!")
    return news

if __name__ == "__main__":
    scrape_times_of_india_news()