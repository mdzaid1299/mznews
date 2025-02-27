from flask import Flask, render_template

app = Flask(__name__)

def load_news():
    try:
        with open("news_data.txt", "r", encoding="utf-8") as file:
            news = []
            for line in file.readlines():
                parts = line.strip().split(' - ')
                if len(parts) == 3:
                    title, link, img_url = parts
                    news.append((title, link, img_url))
            return news
    except FileNotFoundError:
        return []

@app.route('/')
def home():
    news = load_news()
    return render_template('index.html', news=news)

if __name__ == "__main__":
    app.run(debug=True)
