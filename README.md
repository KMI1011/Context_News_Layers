# Context & NewsFeed Layers Integration Guide

This repository contains the **Context Layer** and **News Feed Layer** components of a stock prediction system. This guide explains how to integrate these layers into a larger backend system that merges the 4 core layers for comprehensive stock analysis and prediction.

## Architecture Overview

The stock prediction system is built on a modular architecture with 4 core layers:

### 1. **Context Layer** (`context_layer/`)
   - **Purpose**: Analyzes news sentiment and context for stock symbols
   - **Features**:
     - Fetches company news from StockData.org API (with NewsAPI fallback)
     - Performs sentiment analysis using TextBlob
     - Summarizes news articles (with optional OpenAI GPT integration)
     - Resolves company names to stock symbols
   - **Key Files**:
     - `context_merger.py` - Main orchestration for context analysis
     - `fetch_news.py` - News data fetching
     - `sentiment_engine.py` - Sentiment classification
     - `summarizer.py` - Text summarization (OpenAI)

### 2. **News Feed Layer** (`news_feed_layer/`)
   - **Purpose**: Handles real-time news ingestion and event classification
   - **Features**:
     - Stock data client for fetching market data
     - Event classification (structure ready for implementation)
   - **Key Files**:
     - `stockdata_client.py` - Stock data API client
     - `event_classifiers.py` - Event classification (ready for implementation)

### 3. **Prediction Layer** (to be integrated)
   - **Purpose**: Machine learning models for stock price prediction
   - **Expected Features**:
     - Time series forecasting
     - Feature engineering from context and news data
     - Model training and inference

### 4. **Data/API Layer** (to be integrated)
   - **Purpose**: Data aggregation and API endpoints
   - **Expected Features**:
     - RESTful API endpoints
     - Data persistence (database)
     - Caching layer
     - Request/response handling

## Installation

### Prerequisites
- Python 3.9+
- API keys:
  - `STOCKDATA_API_KEY` - From [StockData.org](https://stockdata.org)
  - `OPENAI_API_KEY` (optional) - For advanced summarization
  - `NEWS_API_KEY` (optional) - Fallback news source

### Setup

1. **Clone the repository** (or add as a submodule to your backend):
```bash
git clone <repository-url>
cd Context_NewsFeed_Layers
```

2. **Create a virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Create a `.env` file** in the root directory:
```env
STOCKDATA_API_KEY=your_stockdata_api_key_here
OPENAI_API_KEY=your_openai_api_key_here  # Optional
NEWS_API_KEY=your_newsapi_key_here       # Optional
```

5. **Test the installation**:
```bash
bash run_test.sh
# Or manually:
python utils/test_context.py
```

## Integration into a Larger Backend

### Step 1: Project Structure

Organize your backend with the following structure:

```
your-backend/
├── layers/
│   ├── context_layer/          # Copy or symlink this directory
│   ├── news_feed_layer/        # Copy or symlink this directory
│   ├── prediction_layer/       # Your ML prediction layer
│   └── data_layer/             # Your data/API layer
├── api/
│   ├── endpoints/
│   │   ├── context.py          # Context analysis endpoints
│   │   ├── news.py             # News feed endpoints
│   │   └── prediction.py       # Prediction endpoints
│   └── main.py                 # FastAPI/Flask app
├── models/                     # Database models
├── services/                   # Business logic
├── utils/                      # Shared utilities
├── requirements.txt
└── .env
```

### Step 2: Import the Layers

#### Option A: As a Python Package

Add the layers to your Python path in your backend's main application:

```python
# api/main.py or your main application file
import sys
from pathlib import Path

# Add layers to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "layers"))

from context_layer.context_merger import analyze_context
from news_feed_layer.stockdata_client import get_company_news
```

#### Option B: As a Git Submodule

If using Git, add this repository as a submodule:

```bash
git submodule add <repository-url> layers/context_newsfeed
```

Then import:
```python
sys.path.insert(0, str(project_root / "layers" / "context_newsfeed"))
```

### Step 3: Create Service Layer

Create a service layer that orchestrates the 4 core layers:

```python
# services/stock_analysis_service.py
from context_layer.context_merger import analyze_context
from news_feed_layer.stockdata_client import get_company_news
# from prediction_layer.predictor import predict_stock_price
# from data_layer.repository import save_analysis

class StockAnalysisService:
    """Service that merges all 4 core layers for comprehensive stock analysis."""
    
    def __init__(self):
        self.context_layer = analyze_context
        self.news_feed_layer = get_company_news
        # self.prediction_layer = predict_stock_price
        # self.data_layer = save_analysis
    
    def analyze_stock(self, symbol: str):
        """
        Comprehensive stock analysis combining all layers.
        
        Args:
            symbol: Stock ticker symbol (e.g., 'AAPL')
            
        Returns:
            dict: Combined analysis from all layers
        """
        # Layer 1: Context Analysis
        context_result = self.context_layer(symbol)
        
        # Layer 2: News Feed
        news_data = self.news_feed_layer(symbol, limit=10)
        
        # Layer 3: Prediction (to be implemented)
        # prediction_result = self.prediction_layer(
        #     symbol=symbol,
        #     context=context_result,
        #     news=news_data
        # )
        
        # Layer 4: Data Persistence (to be implemented)
        # self.data_layer.save({
        #     'symbol': symbol,
        #     'context': context_result,
        #     'news': news_data,
        #     'prediction': prediction_result
        # })
        
        return {
            'symbol': symbol,
            'context': context_result,
            'news': news_data,
            # 'prediction': prediction_result,
            'timestamp': datetime.utcnow().isoformat()
        }
```

### Step 4: Create API Endpoints

#### FastAPI Example

```python
# api/endpoints/stock.py
from fastapi import APIRouter, HTTPException
from services.stock_analysis_service import StockAnalysisService

router = APIRouter(prefix="/api/v1/stocks", tags=["stocks"])
service = StockAnalysisService()

@router.get("/{symbol}/analysis")
async def get_stock_analysis(symbol: str):
    """
    Get comprehensive stock analysis from all 4 layers.
    
    - **Context Layer**: News sentiment and summary
    - **News Feed Layer**: Recent news articles
    - **Prediction Layer**: Price predictions (to be implemented)
    - **Data Layer**: Cached/stored results (to be implemented)
    """
    try:
        result = service.analyze_stock(symbol.upper())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{symbol}/context")
async def get_stock_context(symbol: str):
    """Get context analysis only (Layer 1)."""
    try:
        from context_layer.context_merger import analyze_context
        result = analyze_context(symbol.upper())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{symbol}/news")
async def get_stock_news(symbol: str, limit: int = 10):
    """Get news feed only (Layer 2)."""
    try:
        from news_feed_layer.stockdata_client import get_company_news
        result = get_company_news(symbol.upper(), limit=limit)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

#### Flask Example

```python
# api/endpoints/stock.py
from flask import Blueprint, jsonify, request
from services.stock_analysis_service import StockAnalysisService

bp = Blueprint('stocks', __name__, url_prefix='/api/v1/stocks')
service = StockAnalysisService()

@bp.route('/<symbol>/analysis', methods=['GET'])
def get_stock_analysis(symbol):
    """Get comprehensive stock analysis from all 4 layers."""
    try:
        result = service.analyze_stock(symbol.upper())
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

### Step 5: Environment Configuration

Ensure your backend's `.env` file includes all necessary API keys:

```env
# Context & News Feed Layers
STOCKDATA_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
NEWS_API_KEY=your_key_here

# Database (for Data Layer)
DATABASE_URL=postgresql://user:password@localhost/dbname

# Cache (Redis, optional)
REDIS_URL=redis://localhost:6379

# Other backend configurations
...
```

### Step 6: Error Handling & Logging

Add proper error handling and logging:

```python
# services/stock_analysis_service.py
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class StockAnalysisService:
    def analyze_stock(self, symbol: str) -> dict:
        try:
            # Context Layer with error handling
            try:
                context_result = self.context_layer(symbol)
            except Exception as e:
                logger.error(f"Context layer failed for {symbol}: {e}")
                context_result = {
                    "symbol": symbol,
                    "summary": "Analysis unavailable",
                    "sentiment": "neutral",
                    "sources": []
                }
            
            # News Feed Layer with error handling
            try:
                news_data = self.news_feed_layer(symbol, limit=10)
            except Exception as e:
                logger.error(f"News feed layer failed for {symbol}: {e}")
                news_data = []
            
            # ... other layers
            
            return {
                'symbol': symbol,
                'context': context_result,
                'news': news_data,
                'status': 'success'
            }
        except Exception as e:
            logger.exception(f"Stock analysis failed for {symbol}")
            raise
```

### Step 7: Caching (Optional but Recommended)

Implement caching to reduce API calls:

```python
# services/stock_analysis_service.py
from functools import lru_cache
import redis
import json

class StockAnalysisService:
    def __init__(self, redis_client=None):
        self.redis = redis_client
        self.cache_ttl = 3600  # 1 hour
    
    def analyze_stock(self, symbol: str, use_cache: bool = True):
        # Check cache first
        if use_cache and self.redis:
            cached = self.redis.get(f"stock:{symbol}:analysis")
            if cached:
                return json.loads(cached)
        
        # Perform analysis
        result = self._perform_analysis(symbol)
        
        # Cache result
        if use_cache and self.redis:
            self.redis.setex(
                f"stock:{symbol}:analysis",
                self.cache_ttl,
                json.dumps(result)
            )
        
        return result
```

## Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                      API Request                            │
│                   (GET /stocks/AAPL/analysis)               │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                 StockAnalysisService                        │
│              (Orchestrates all 4 layers)                    │
└──────┬──────────────────┬──────────────────┬────────────────┘
       │                  │                  │
       ▼                  ▼                  ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   Layer 1    │  │   Layer 2    │  │   Layer 3    │
│   Context    │  │  News Feed   │  │  Prediction  │
│              │  │              │  │              │
│ - News Fetch │  │ - Real-time  │  │ - ML Models  │
│ - Sentiment  │  │   Ingestion  │  │ - Forecasting│
│ - Summary    │  │ - Events     │  │ - Features   │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                  │                  │
       └──────────────────┼──────────────────┘
                          │
                          ▼
                ┌──────────────────┐
                │   Layer 4        │
                │   Data/API       │
                │                  │
                │ - Persistence    │
                │ - Caching        │
                │ - Response       │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │   API Response   │
                │   (JSON)         │
                └──────────────────┘
```

## Testing

### Unit Tests

Test each layer independently:

```python
# tests/test_context_layer.py
import unittest
from context_layer.context_merger import analyze_context

class TestContextLayer(unittest.TestCase):
    def test_analyze_context(self):
        result = analyze_context("AAPL")
        self.assertIn('symbol', result)
        self.assertIn('sentiment', result)
        self.assertIn(result['sentiment'], ['positive', 'negative', 'neutral'])
```

### Integration Tests

Test the service layer:

```python
# tests/test_stock_analysis_service.py
import unittest
from services.stock_analysis_service import StockAnalysisService

class TestStockAnalysisService(unittest.TestCase):
    def setUp(self):
        self.service = StockAnalysisService()
    
    def test_analyze_stock(self):
        result = self.service.analyze_stock("AAPL")
        self.assertIn('symbol', result)
        self.assertIn('context', result)
        self.assertIn('news', result)
```

## Performance Considerations

1. **Rate Limiting**: Implement rate limiting for API endpoints to prevent abuse
2. **Async Processing**: Use async/await for I/O-bound operations (news fetching)
3. **Background Jobs**: Use Celery or similar for long-running predictions
4. **Caching**: Cache results to reduce API calls and improve response times
5. **Batch Processing**: Process multiple symbols in batches when possible

## Next Steps

1. **Implement Prediction Layer**: Add ML models for stock price forecasting
2. **Implement Data Layer**: Add database persistence and caching
3. **Add Authentication**: Secure your API endpoints
4. **Add Monitoring**: Implement logging, metrics, and alerting
5. **Add Documentation**: Use OpenAPI/Swagger for API documentation
6. **Add Tests**: Comprehensive unit and integration tests

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure the layers are in your Python path
2. **API Key Errors**: Verify `.env` file is loaded correctly
3. **Network Errors**: Check API rate limits and network connectivity
4. **Dependency Conflicts**: Use virtual environments to isolate dependencies

### Debugging

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

When adding new features:
1. Follow the layer architecture
2. Add appropriate error handling
3. Write tests for new functionality
4. Update this README if needed


