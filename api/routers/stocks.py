from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from models.stock import StockData, StockQuote, StockHistory
from services import StockService

router = APIRouter()


@router.get("/{symbol}", response_model=StockData)
async def get_stock_data(symbol: str):
    """
    Get comprehensive stock data for a symbol
    
    - **symbol**: Stock ticker symbol (e.g., AAPL, GOOGL, TSLA)
    """
    try:
        return StockService.get_stock_data(symbol)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stock data: {str(e)}")


@router.get("/{symbol}/quote", response_model=StockQuote)
async def get_stock_quote(symbol: str):
    """
    Get real-time quote for a stock
    
    - **symbol**: Stock ticker symbol
    """
    try:
        return StockService.get_quote(symbol)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching quote: {str(e)}")


@router.get("/{symbol}/history", response_model=StockHistory)
async def get_stock_history(
    symbol: str,
    period: str = Query(default="1mo", description="Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, max)"),
    interval: str = Query(default="1d", description="Data interval (1m, 5m, 15m, 30m, 1h, 1d, 1wk, 1mo)")
):
    """
    Get historical stock data
    
    - **symbol**: Stock ticker symbol
    - **period**: Time period for historical data
    - **interval**: Data point interval
    """
    try:
        return StockService.get_history(symbol, period, interval)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching history: {str(e)}")


@router.get("/search/{query}")
async def search_stocks(
    query: str,
    limit: int = Query(default=10, ge=1, le=50)
):
    """
    Search for stock symbols
    
    - **query**: Search query
    - **limit**: Maximum number of results (1-50)
    """
    try:
        return StockService.search_symbols(query, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching stocks: {str(e)}")
