from datetime import datetime
from typing import Optional, List
import ccxt
from models.crypto import CryptoData, CryptoHistory, CryptoListItem
from models.common import DataPoint


class CryptoService:
    """Service for fetching cryptocurrency data using CCXT"""
    
    def __init__(self, exchange_id: str = 'binance'):
        """
        Initialize crypto service with exchange
        
        Args:
            exchange_id: Exchange identifier (default: binance)
        """
        exchange_class = getattr(ccxt, exchange_id)
        self.exchange = exchange_class({
            'enableRateLimit': True,
        })
    
    def get_crypto_data(self, symbol: str) -> CryptoData:
        """
        Get real-time cryptocurrency data
        
        Args:
            symbol: Crypto trading pair (e.g., 'BTC/USDT', 'ETH/USDT')
            
        Returns:
            CryptoData object with current market data
        """
        # Normalize symbol format
        if '/' not in symbol:
            symbol = f"{symbol.upper()}/USDT"
        
        # Get ticker data
        ticker = self.exchange.fetch_ticker(symbol)
        
        # Get 24h OHLCV for additional metrics
        ohlcv = self.exchange.fetch_ohlcv(symbol, '1d', limit=2)
        
        previous_close = ohlcv[0][4] if len(ohlcv) > 1 else ticker['last']
        current_price = ticker['last']
        change_24h = current_price - previous_close
        change_percent_24h = (change_24h / previous_close * 100) if previous_close else 0
        
        return CryptoData(
            symbol=symbol,
            name=symbol.split('/')[0],
            price=current_price,
            change_24h=change_24h,
            change_percent_24h=change_percent_24h,
            volume_24h=ticker.get('quoteVolume', 0),
            high_24h=ticker.get('high'),
            low_24h=ticker.get('low'),
            timestamp=datetime.fromtimestamp(ticker['timestamp'] / 1000)
        )
    
    def get_history(
        self,
        symbol: str,
        timeframe: str = '1d',
        limit: int = 100
    ) -> CryptoHistory:
        """
        Get historical cryptocurrency data
        
        Args:
            symbol: Crypto trading pair (e.g., 'BTC/USDT')
            timeframe: Timeframe (1m, 5m, 15m, 30m, 1h, 4h, 1d, 1w, 1M)
            limit: Number of data points to retrieve
            
        Returns:
            CryptoHistory object with historical data
        """
        # Normalize symbol format
        if '/' not in symbol:
            symbol = f"{symbol.upper()}/USDT"
        
        # Fetch OHLCV data
        ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        
        if not ohlcv:
            raise ValueError(f"No historical data available for {symbol}")
        
        data_points = []
        for candle in ohlcv:
            data_points.append(DataPoint(
                timestamp=datetime.fromtimestamp(candle[0] / 1000),
                open=float(candle[1]),
                high=float(candle[2]),
                low=float(candle[3]),
                close=float(candle[4]),
                volume=float(candle[5])
            ))
        
        return CryptoHistory(
            symbol=symbol,
            data_points=data_points,
            start_date=data_points[0].timestamp,
            end_date=data_points[-1].timestamp,
            interval=timeframe
        )
    
    def list_cryptocurrencies(self, limit: int = 100) -> List[CryptoListItem]:
        """
        List available cryptocurrencies
        
        Args:
            limit: Maximum number of cryptos to return
            
        Returns:
            List of CryptoListItem objects
        """
        markets = self.exchange.load_markets()
        
        # Filter for USDT pairs
        usdt_pairs = [
            symbol for symbol in markets.keys()
            if '/USDT' in symbol
        ][:limit]
        
        crypto_list = []
        for symbol in usdt_pairs:
            base_currency = symbol.split('/')[0]
            try:
                ticker = self.exchange.fetch_ticker(symbol)
                crypto_list.append(CryptoListItem(
                    symbol=symbol,
                    name=base_currency,
                    price=ticker.get('last'),
                ))
            except Exception:
                # Skip if unable to fetch ticker
                continue
        
        return crypto_list
    
    def search_symbols(self, query: str, limit: int = 10) -> List[dict]:
        """
        Search for cryptocurrency symbols
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of matching symbols
        """
        markets = self.exchange.load_markets()
        query_upper = query.upper()
        
        matching_symbols = [
            {
                'symbol': symbol,
                'name': symbol.split('/')[0],
                'exchange': self.exchange.id,
                'type': 'crypto'
            }
            for symbol in markets.keys()
            if query_upper in symbol.upper()
        ][:limit]
        
        return matching_symbols
