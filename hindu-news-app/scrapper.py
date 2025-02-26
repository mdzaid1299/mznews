import requests
from bs4 import BeautifulSoup

def scrape_times_of_india_news():
    url = "https://timesofindia.indiatimes.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Adjust the selectors based on the new structure
    articles = soup.select("div.Bw78m.cardactive")

    # Extract title, link, and image for each headline
    news = []
    for article in articles:
        img_tag = article.find("img")
        title_tag = article.find_next("figcaption")
        link_tag = article.find("a")

        title = title_tag.text.strip() if title_tag else "No title available"
        link = link_tag['href'] if link_tag and link_tag.get('href') else "No link available"
        link = link if link.startswith("https") else f"{url.rstrip('/')}{link}" if link != "No link available" else link
        img_src = img_tag['data-src'] if img_tag and img_tag.get('data-src') else img_tag['src'] if img_tag and img_tag.get('src') else "No image available"
        
        news.append({"title": title, "link": link, "image": img_src})

    # Save data to file
    with open("news_data.txt", "w", encoding="utf-8") as file:
        for item in news:
            file.write(f"{item['title']} - {item['link']} - {item['image']}\n")

    print(f"Scraped {len(news)} headlines!")
    return news

if __name__ == "__main__":
    scrape_times_of_india_news()
