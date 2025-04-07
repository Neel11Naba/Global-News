from flask import Flask, render_template, request
import requests
import os
from datetime import datetime

app = Flask(__name__)

NEWS_API_KEY = os.environ.get("NEWS_API_KEY")  # Use Render env var

BASE_URL = "https://newsapi.org/v2/top-headlines"

def get_news(query=None, category=None, country='us'):
    params = {
        "apiKey": NEWS_API_KEY,
        "country": country,
        "pageSize": 20,
    }

    if query:
        params["q"] = query
    if category and category != "all":
        params["category"] = category

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        articles = data.get("articles", [])

        for article in articles:
            published_at = article.get("publishedAt")
            if published_at:
                dt_obj = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ")
                article["publishedAt"] = dt_obj.strftime("%d %b %Y, %I:%M %p")

        return articles
    except Exception as e:
        print("Error fetching news:", e)
        return []

@app.route("/")
def home():
    query = request.args.get("q")
    selected_category = request.args.get("category", "business")
    
    #Show indian stock market news by default
    if not query :
        query= "indian stock market "
        
    articles = get_news(query=query or "indian stock market", category=selected_category)
    categories = ["business", "technology", "entertainment", "health", "science", "sports"]
    return render_template("index.html", articles=articles, categories=categories, selected_category=selected_category)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/disclaimer")
def disclaimer():
    return render_template("disclaimer.html")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
