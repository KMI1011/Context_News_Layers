# context_layer/summarizer.py

from openai import OpenAI
from utils.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def summarize_text(text: str) -> str:
    """
    Use GPT model to summarize stock-related news text.
    """
    if not text:
        return "No text provided."

    prompt = f"Summarize this financial news in under 100 words:\n\n{text[:4000]}"
    try:
        response = client.responses.create(
            model="gpt-4o-mini",
            input=prompt,
            max_output_tokens=150
        )
        return response.output[0].content[0].text.strip()
    except Exception as e:
        print(f"❌ Summarization failed: {e}")
        return "Summary unavailable."
