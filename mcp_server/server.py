import sys
import os

# Add parent directory to path to import services
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastmcp import FastMCP
from services import StockService, CryptoService

# Initialize services
stock_service = StockService()
crypto_service = CryptoService()

# Create FastMCP server
mcp = FastMCP("trading-data-mcp")


# Stock data tools
@mcp.tool()
def get_stock_data(symbol: str) -> dict:
    """
    Get comprehensive stock market data including price, volume, market cap, and financial metrics.
    
    Args:
        symbol: Stock ticker symbol (e.g., AAPL, GOOGL, TSLA)
    
    Returns:
        Comprehensive stock data including current quote and financial information
    """
    try:
        data = stock_service.get_stock_data(symbol)
        return data.model_dump()
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_stock_quote(symbol: str) -> dict:
    """
    Get real-time stock quote with current price and trading information.
    
    Args:
        symbol: Stock ticker symbol
    
    Returns:
        Real-time quote with price, volume, and change information
    """
    try:
        quote = stock_service.get_quote(symbol)
        return quote.model_dump()
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_stock_history(symbol: str, period: str = "1mo", interval: str = "1d") -> dict:
    """
    Get historical stock price data with OHLCV (Open, High, Low, Close, Volume).
    
    Args:
        symbol: Stock ticker symbol
        period: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, max). Default: 1mo
        interval: Data interval (1m, 5m, 15m, 30m, 1h, 1d, 1wk, 1mo). Default: 1d
    
    Returns:
        Historical price data with OHLCV candles
    """
    try:
        history = stock_service.get_history(symbol, period, interval)
        return history.model_dump()
    except Exception as e:
        return {"error": str(e)}


# Cryptocurrency data tools
@mcp.tool()
def get_crypto_data(symbol: str) -> dict:
    """
    Get real-time cryptocurrency market data including price, volume, and market metrics.
    
    Args:
        symbol: Crypto symbol or trading pair (e.g., BTC, ETH, BTC/USDT)
    
    Returns:
        Current cryptocurrency market data
    """
    try:
        data = crypto_service.get_crypto_data(symbol)
        return data.model_dump()
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_crypto_history(symbol: str, timeframe: str = "1d", limit: int = 100) -> dict:
    """
    Get historical cryptocurrency price data with OHLCV candles.
    
    Args:
        symbol: Crypto symbol or trading pair
        timeframe: Candle timeframe (1m, 5m, 15m, 30m, 1h, 4h, 1d, 1w, 1M). Default: 1d
        limit: Number of data points to retrieve. Default: 100
    
    Returns:
        Historical cryptocurrency price data
    """
    try:
        history = crypto_service.get_history(symbol, timeframe, limit)
        return history.model_dump()
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def list_cryptocurrencies(limit: int = 100) -> dict:
    """
    List available cryptocurrencies with basic information.
    
    Args:
        limit: Maximum number of cryptocurrencies to return. Default: 100
    
    Returns:
        List of available cryptocurrencies
    """
    try:
        cryptos = crypto_service.list_cryptocurrencies(limit)
        return {"cryptocurrencies": [c.model_dump() for c in cryptos]}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def search_symbols(query: str, asset_type: str = "stock", limit: int = 10) -> dict:
    """
    Search for stock or cryptocurrency symbols.
    
    Args:
        query: Search query
        asset_type: Type of asset to search (stock or crypto). Default: stock
        limit: Maximum number of results. Default: 10
    
    Returns:
        List of matching symbols
    """
    try:
        if asset_type == "stock":
            results = stock_service.search_symbols(query, limit)
        else:
            results = crypto_service.search_symbols(query, limit)
        return {"results": results}
    except Exception as e:
        return {"error": str(e)}


def run_mcp_http_server(host: str = "0.0.0.0", port: int = 8001):
    """Run the MCP server with FastMCP using streamable-http transport"""
    mcp.run(transport="streamable-http", host=host, port=port)


if __name__ == "__main__":
    run_mcp_http_server()
