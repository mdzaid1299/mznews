from flask import Flask

app = Flask(__name__)

def load_news():
    try:
        with open("news_data.txt", "r") as file:
            return file.readlines()
    except FileNotFoundError:
        return ["No news available."]

@app.route('/')
def home():
    news = load_news()
    return "<br>".join(news)

if __name__ == "__main__":
    app.run(debug=True)
