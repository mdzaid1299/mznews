import os
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

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

@app.route('/api/more-news')
def more_news():
    page = int(request.args.get('page', 1))
    news = load_news()
    
    # Calculate start and end indices for pagination
    # Page 1 is already shown in the main page (items 0-9)
    start_idx = page * 10
    end_idx = start_idx + 10
    
    # Check if there are more items after this batch
    has_more = len(news) > end_idx
    
    # Return the news items for this page
    return jsonify({
        'news': news[start_idx:end_idx] if start_idx < len(news) else [],
        'has_more': has_more
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)