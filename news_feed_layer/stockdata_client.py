import requests
from utils.config import STOCKDATA_API_KEY

BASE_URL = "https://api.stockdata.org/v1"

def get_company_news(symbol="AAPL", limit=5):
    """
    Fetch latest company news using StockData.org API.
    """
    url = f"{BASE_URL}/news/all?symbols={symbol}&limit={limit}&api_token={STOCKDATA_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if "data" in data:
            return [article["title"] + " " + (article.get("description") or "") for article in data["data"]]
        else:
            print("⚠️ No news data returned.")
            return []
    else:
        print(f"Error {response.status_code}: {response.text}")
        return []
