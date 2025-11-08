# context_layer/news_ingestion.py

import requests
from utils.config import STOCKDATA_API_KEY

def fetch_news_for_symbol(symbol: str, limit: int = 5):
    """
    Fetch recent news articles for a given stock symbol from StockData.org API.
    
    Args:
        symbol (str): The stock ticker (e.g., 'AAPL').
        limit (int): Number of articles to fetch.
    
    Returns:
        dict: JSON response from the API or an empty list if failed.
    """
    try:
        url = f"https://api.stockdata.org/v1/news/all?symbols={symbol}&limit={limit}&api_token={STOCKDATA_API_KEY}"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"⚠️ Error {response.status_code}: {response.text}")
            return {"data": []}
    except Exception as e:
        print(f"❌ Error fetching news: {e}")
        return {"data": []}
