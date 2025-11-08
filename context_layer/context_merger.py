# context_layer/context_merger.py

import requests
from textblob import TextBlob
from .fetch_news import get_company_news
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

# Optional: if you want to auto-resolve names like "Apple" → "AAPL"
def resolve_symbol(company_name: str) -> str:
    api_token = os.getenv("STOCKDATA_API_KEY")
    if not api_token:
        # If no API key, return the company name as-is (uppercase if it looks like a symbol)
        return company_name.upper() if len(company_name) <= 5 and company_name.isalpha() else company_name
    
    url = f"https://api.stockdata.org/v1/entity/search?search={company_name}&api_token={api_token}"
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("data"):
                return data["data"][0]["symbol"]
    except Exception as e:
        print(f"⚠️ Error resolving symbol: {e}")
    return company_name  # fallback if API fails


def analyze_context(symbol_or_name: str):
    """
    Fetches company news, summarizes it, and classifies sentiment.
    """
    symbol = resolve_symbol(symbol_or_name) or symbol_or_name.upper()
    if len(symbol) > 5 and not symbol.isupper():  # crude check
        symbol = symbol_or_name.upper()

    print(f"🧠 Running context analysis for {symbol} ...")

    # Step 1: Fetch news
    news_data = get_company_news(symbol)
    if not news_data or len(news_data) == 0:
        return {
            "symbol": symbol_or_name,
            "summary": "No news found.",
            "sentiment": "neutral",
            "sources": []
        }

    # Step 2: Summarize text
    summaries = [n["title"] + " " + n.get("description", "") for n in news_data if n.get("title")]
    full_text = " ".join(summaries)[:4000]  # Limit to safe token size
    summary = summarize_text(full_text)

    # Step 3: Classify sentiment
    sentiment = classify_sentiment(full_text)

    # Step 4: Package structured output
    return {
        "symbol": symbol_or_name,
        "summary": summary,
        "sentiment": sentiment,
        "sources": [n["url"] for n in news_data if "url" in n]
    }


def summarize_text(text):
    """
    Simple summarizer placeholder. Replace with OpenAI or your own model if needed.
    """
    if not text:
        return "No summary available."
    # For simplicity using TextBlob’s basic noun phrase extraction
    blob = TextBlob(text)
    sentences = blob.sentences
    return " ".join(str(s) for s in sentences[:3])  # first 3 sentences


def classify_sentiment(text):
    """
    Uses TextBlob polarity score to classify sentiment.
    """
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.1:
        return "positive"
    elif polarity < -0.1:
        return "negative"
    return "neutral"
