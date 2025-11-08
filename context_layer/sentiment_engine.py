# context_layer/sentiment_engine.py

from textblob import TextBlob

def classify_sentiment(text: str) -> str:
    """
    Simple sentiment classification for summarized news.
    Returns: 'positive', 'neutral', or 'negative'.
    """
    if not text:
        return "neutral"

    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.2:
        return "positive"
    elif polarity < -0.2:
        return "negative"
    else:
        return "neutral"
