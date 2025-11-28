from fastapi import APIRouter, HTTPException, Query
from typing import List
from models.crypto import CryptoData, CryptoHistory, CryptoListItem
from services import CryptoService

router = APIRouter()

# Initialize crypto service
crypto_service = CryptoService()


@router.get("/{symbol}", response_model=CryptoData)
async def get_crypto_data(symbol: str):
    """
    Get real-time cryptocurrency data
    
    - **symbol**: Crypto symbol or trading pair (e.g., BTC, ETH, BTC/USDT)
    """
    try:
        return crypto_service.get_crypto_data(symbol)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching crypto data: {str(e)}")


@router.get("/{symbol}/history", response_model=CryptoHistory)
async def get_crypto_history(
    symbol: str,
    timeframe: str = Query(default="1d", description="Timeframe (1m, 5m, 15m, 30m, 1h, 4h, 1d, 1w, 1M)"),
    limit: int = Query(default=100, ge=1, le=1000, description="Number of data points")
):
    """
    Get historical cryptocurrency data
    
    - **symbol**: Crypto symbol or trading pair
    - **timeframe**: Candle timeframe
    - **limit**: Number of data points to retrieve
    """
    try:
        return crypto_service.get_history(symbol, timeframe, limit)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching history: {str(e)}")


@router.get("/list/all", response_model=List[CryptoListItem])
async def list_cryptocurrencies(
    limit: int = Query(default=100, ge=1, le=500)
):
    """
    List available cryptocurrencies
    
    - **limit**: Maximum number of cryptos to return (1-500)
    """
    try:
        return crypto_service.list_cryptocurrencies(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing cryptocurrencies: {str(e)}")


@router.get("/search/{query}")
async def search_crypto(
    query: str,
    limit: int = Query(default=10, ge=1, le=50)
):
    """
    Search for cryptocurrency symbols
    
    - **query**: Search query
    - **limit**: Maximum number of results (1-50)
    """
    try:
        return crypto_service.search_symbols(query, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching crypto: {str(e)}")
