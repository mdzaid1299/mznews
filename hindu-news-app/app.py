import os
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)
CORS(app)

def load_news():
    response = supabase.table("news").select("*").order("created_at", desc=True).execute()
    data = response.data
    return [(item["title"], item["link"], item["image_url"]) for item in data]

@app.route('/')
def home():
    news = load_news()[:10]  # Load only first 10 items for homepage
    return render_template('index.html', news=news)

@app.route('/api/more-news')
def more_news():
    page = int(request.args.get('page', 1))
    news = load_news()

    # Pagination logic: 10 items per page
    start_idx = page * 10
    end_idx = start_idx + 10
    has_more = len(news) > end_idx

    return jsonify({
        'news': news[start_idx:end_idx] if start_idx < len(news) else [],
        'has_more': has_more
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
