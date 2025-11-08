# context_layer/fetch_news.py

import requests
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file in the project root
# Try multiple paths to ensure we find the .env file
project_root = Path(__file__).parent.parent
env_path = project_root / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    # Fallback: try loading from current directory
    load_dotenv(dotenv_path='.env')

def get_company_news(symbol: str):
    """
    Fetches company news from StockData.org.
    Falls back to NewsAPI if StockData.org returns no data.
    """
    api_token = os.getenv("STOCKDATA_API_KEY")
    if not api_token:
        print("⚠️ Warning: Missing STOCKDATA_API_KEY in environment variables")
        print("💡 To use this feature, create a .env file in the project root with:")
        print("   STOCKDATA_API_KEY=your_api_key_here")
        return []

    # Try StockData.org
    url = f"https://api.stockdata.org/v1/news/all?symbols={symbol}&language=en&api_token={api_token}"
    try:
        print(f"📰 Fetching company news from StockData.org for {symbol}...")
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json().get("data", [])
            if data:
                return data
        else:
            print(f"⚠️ StockData.org error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"⚠️ StockData.org request failed: {e}")

    # Fallback to NewsAPI
    newsapi_key = os.getenv("NEWS_API_KEY")
    if newsapi_key:
        print(f"🗞️ Falling back to NewsAPI for {symbol}...")
        try:
            url = f"https://newsapi.org/v2/everything?q={symbol}&language=en&sortBy=publishedAt&apiKey={newsapi_key}"
            response = requests.get(url)
            if response.status_code == 200:
                articles = response.json().get("articles", [])
                formatted = [
                    {
                        "title": a["title"],
                        "description": a.get("description", ""),
                        "url": a["url"]
                    }
                    for a in articles
                ]
                return formatted
        except Exception as e:
            print(f"⚠️ NewsAPI fallback failed: {e}")

    print("⚠️ No data returned from any source.")
    return []
