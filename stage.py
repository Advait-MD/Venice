from flask import Flask, jsonify, render_template
import requests
import uuid
import spacy
from geopy.geocoders import Nominatim

nlp = spacy.load("en_core_web_sm")  

app = Flask(__name__)
API_KEY = 'a99f1842e87946c482e3731fa59f4256'

"""# Mapping of categories to API parameters
NEWS_CATEGORIES = {
    'sports': 'sports',
    'technology': 'technology',
    'politics': 'general'  # no direct 'politics' category, use 'general' + keyword
}"""

url = f'https://newsapi.org/v2/top-headlines?category=sports&apiKey={API_KEY}'

response = requests.get(url)
data = response.json()

articles = []
if data.get("status") == "ok":
      articles.append({
                "id": str(uuid.uuid4()),
                "title": article.get("title", "No Title"),
                "url": article.get("url", "#")
            })

    return jsonify({"articles": articles})



if __name__ == "__main__":
    app.run(debug=True)
