from flask import Flask, jsonify, render_template
import requests
import uuid
app = Flask(__name__)
API_KEY = 'a99f1842e87946c482e3731fa59f4256'

# Mapping of categories to API parameters
NEWS_CATEGORIES = {
    'sports': 'sports',
    'technology': 'technology',
    'politics': 'general'  # no direct 'politics' category, use 'general' + keyword
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-news/<category>')
def get_news(category):
    category = category.lower()
    if category not in NEWS_CATEGORIES:
        return jsonify({"error": "Invalid category"}), 400

    url = f'https://newsapi.org/v2/top-headlines?category={category}&apiKey={API_KEY}'

    # Modify for politics to filter only political articles
    if category == 'politics':
        url += '&q=general'
    else:
        url += f"&category={NEWS_CATEGORIES[category]}"

    response = requests.get(url)
    data = response.json()

    articles = []
    if data.get("status") == "ok":
        for article in data.get("articles", [])[:5]:
            articles.append({
                "id": str(uuid.uuid4()),
                "title": article.get("title", "No Title"),
                "url": article.get("url", "#")
            })

    return jsonify({"articles": articles})



if __name__ == "__main__":
    app.run(debug=True)
