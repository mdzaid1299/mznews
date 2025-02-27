# Times of India News Scraper

## Project Overview
This project is a **web scraping script** that extracts the latest news headlines, links, and images from the [Times of India](https://timesofindia.indiatimes.com/) homepage. The scraped data is saved into a `news_data.txt` file for further use.

## How the Scraper Works
The scraper is built using **Python** with the **requests** and **BeautifulSoup** libraries.

### 1. HTTP Request
```python
response = requests.get(url)
```
The script sends an HTTP GET request to the Times of India website and retrieves the HTML content.

### 2. Parsing HTML
```python
soup = BeautifulSoup(response.content, "html.parser")
```
The HTML content is parsed using BeautifulSoup, allowing easy navigation and extraction of elements.

### 3. Selecting News Articles
```python
articles = soup.select("figure a")
```
We use the `select()` method with CSS selectors to target the links inside `figure` tags, as seen in the website's structure.

### 4. Extracting Data
- **Title** is extracted using `find_next("figcaption")`, as per the site's layout.
- **Link** comes from the `href` attribute of the `<a>` tag.
- **Image** is sourced from either the `data-src` or `src` attribute of the nested `<img>` tag.

```python
title_tag = article.find_next("figcaption")
link = article['href'] if article.get('href') else "No link available"
img_src = img_tag['data-src'] if img_tag and img_tag.get('data-src') else img_tag['src'] if img_tag and img_tag.get('src') else "No image available"
```

### 5. Saving to File
```python
with open("news_data.txt", "w", encoding="utf-8") as file:
    for item in news:
        file.write(f"{item['title']} - {item['link']} - {item['image']}\n")
```
All the scraped data is formatted and written to a text file for later access.

## Running the Scraper
Ensure you have **Python** installed along with the necessary libraries:

```bash
pip install requests beautifulsoup4
```

Then run the script:

```bash
python scraper.py
```

The data will be saved in `news_data.txt`.

## Deployment
The scraper can be deployed using **Render** or **GitHub Actions** for automation. The goal is to scrape news at regular intervals and update the data automatically.

## Deployed Link
The deployed scraper is live at:
[mznews](https://mznews.onrender.com/)

## Future Enhancements
- **Database Integration:** Store news data in a database instead of a text file.
- **Automation:** Add a cron job or GitHub Actions to scrape data daily.

---

Feel free to clone, modify, and extend the project!

## License
This project is licensed under the MIT License.
