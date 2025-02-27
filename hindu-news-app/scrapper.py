import requests
from bs4 import BeautifulSoup

def scrape_times_of_india_news():
    url = "https://timesofindia.indiatimes.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Updated selector for links and images, keeping old title logic
    articles = soup.select("figure a")

    # Extract title, link, and image for each headline
    news = []
    for article in articles:
        img_tag = article.find("img")
        title_tag = article.find_next("figcaption")  # Your old title logic
        link = article['href'] if article.get('href') else "No link available"
        link = link if link.startswith("https") else f"{url.rstrip('/')}{link}" if link != "No link available" else link
        img_src = img_tag['data-src'] if img_tag and img_tag.get('data-src') else img_tag['src'] if img_tag and img_tag.get('src') else "No image available"
        title = title_tag.text.strip() if title_tag else "No title available"

        news.append({"title": title, "link": link, "image": img_src})

    # Save data to file
    with open("news_data.txt", "w", encoding="utf-8") as file:
        for item in news:
            file.write(f"{item['title']} - {item['link']} - {item['image']}\n")

    print(f"Scraped {len(news)} headlines!")
    return news

if __name__ == "__main__":
    scrape_times_of_india_news()
