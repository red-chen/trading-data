from datetime import datetime
from typing import Optional, List
import yfinance as yf
from models.stock import StockData, StockQuote, StockHistory
from models.common import DataPoint, MarketStatus, TimeRange, Interval


class StockService:
    """Service for fetching stock market data using yfinance"""
    
    @staticmethod
    def get_stock_data(symbol: str) -> StockData:
        """
        Get comprehensive stock data for a symbol
        
        Args:
            symbol: Stock ticker symbol (e.g., 'AAPL', 'GOOGL')
            
        Returns:
            StockData object with comprehensive information
        """
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        # Get current quote
        hist = ticker.history(period="1d")
        if hist.empty:
            raise ValueError(f"No data available for symbol {symbol}")
        
        current_price = hist['Close'].iloc[-1]
        previous_close = info.get('previousClose', current_price)
        change = current_price - previous_close
        change_percent = (change / previous_close * 100) if previous_close else 0
        
        quote = StockQuote(
            symbol=symbol.upper(),
            name=info.get('longName'),
            price=float(current_price),
            change=float(change),
            change_percent=float(change_percent),
            volume=int(hist['Volume'].iloc[-1]) if not hist['Volume'].empty else 0,
            market_cap=info.get('marketCap'),
            pe_ratio=info.get('trailingPE'),
            day_high=info.get('dayHigh'),
            day_low=info.get('dayLow'),
            year_high=info.get('fiftyTwoWeekHigh'),
            year_low=info.get('fiftyTwoWeekLow'),
            timestamp=datetime.now()
        )
        
        stock_data = StockData(
            symbol=symbol.upper(),
            name=info.get('longName'),
            exchange=info.get('exchange'),
            currency=info.get('currency'),
            quote=quote,
            sector=info.get('sector'),
            industry=info.get('industry'),
            description=info.get('longBusinessSummary'),
            website=info.get('website'),
            market_cap=info.get('marketCap'),
            enterprise_value=info.get('enterpriseValue'),
            trailing_pe=info.get('trailingPE'),
            forward_pe=info.get('forwardPE'),
            peg_ratio=info.get('pegRatio'),
            price_to_book=info.get('priceToBook'),
            price_to_sales=info.get('priceToSalesTrailing12Months'),
            dividend_rate=info.get('dividendRate'),
            dividend_yield=info.get('dividendYield'),
            beta=info.get('beta'),
            fifty_day_average=info.get('fiftyDayAverage'),
            two_hundred_day_average=info.get('twoHundredDayAverage')
        )
        
        return stock_data
    
    @staticmethod
    def get_quote(symbol: str) -> StockQuote:
        """
        Get real-time quote for a stock
        
        Args:
            symbol: Stock ticker symbol
            
        Returns:
            StockQuote object
        """
        ticker = yf.Ticker(symbol)
        info = ticker.info
        hist = ticker.history(period="1d")
        
        if hist.empty:
            raise ValueError(f"No data available for symbol {symbol}")
        
        current_price = hist['Close'].iloc[-1]
        previous_close = info.get('previousClose', current_price)
        change = current_price - previous_close
        change_percent = (change / previous_close * 100) if previous_close else 0
        
        return StockQuote(
            symbol=symbol.upper(),
            name=info.get('longName'),
            price=float(current_price),
            change=float(change),
            change_percent=float(change_percent),
            volume=int(hist['Volume'].iloc[-1]) if not hist['Volume'].empty else 0,
            market_cap=info.get('marketCap'),
            pe_ratio=info.get('trailingPE'),
            day_high=info.get('dayHigh'),
            day_low=info.get('dayLow'),
            year_high=info.get('fiftyTwoWeekHigh'),
            year_low=info.get('fiftyTwoWeekLow'),
            timestamp=datetime.now()
        )
    
    @staticmethod
    def get_history(
        symbol: str,
        period: str = "1mo",
        interval: str = "1d"
    ) -> StockHistory:
        """
        Get historical stock data
        
        Args:
            symbol: Stock ticker symbol
            period: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, max)
            interval: Data interval (1m, 5m, 15m, 30m, 1h, 1d, 1wk, 1mo)
            
        Returns:
            StockHistory object with historical data points
        """
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period, interval=interval)
        
        if hist.empty:
            raise ValueError(f"No historical data available for symbol {symbol}")
        
        data_points = []
        for timestamp, row in hist.iterrows():
            data_points.append(DataPoint(
                timestamp=timestamp.to_pydatetime(),
                open=float(row['Open']),
                high=float(row['High']),
                low=float(row['Low']),
                close=float(row['Close']),
                volume=float(row['Volume'])
            ))
        
        return StockHistory(
            symbol=symbol.upper(),
            data_points=data_points,
            start_date=hist.index[0].to_pydatetime(),
            end_date=hist.index[-1].to_pydatetime(),
            interval=interval
        )
    
    @staticmethod
    def search_symbols(query: str, limit: int = 10) -> List[dict]:
        """
        Search for stock symbols
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of matching symbols with basic info
        """
        # Note: yfinance doesn't have built-in search, so this is a simple implementation
        # In production, you might want to use a dedicated API like Alpha Vantage or IEX
        try:
            ticker = yf.Ticker(query.upper())
            info = ticker.info
            
            if info and 'symbol' in info:
                return [{
                    'symbol': info.get('symbol', query.upper()),
                    'name': info.get('longName', ''),
                    'exchange': info.get('exchange', ''),
                    'type': 'stock'
                }]
        except Exception:
            pass
        
        return []
