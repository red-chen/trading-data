from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict, field_serializer
from .common import DataPoint, MarketStatus


class StockQuote(BaseModel):
    """Real-time stock quote"""
    symbol: str
    name: Optional[str] = None
    price: float
    change: float
    change_percent: float
    volume: int
    market_cap: Optional[float] = None
    pe_ratio: Optional[float] = None
    day_high: Optional[float] = None
    day_low: Optional[float] = None
    year_high: Optional[float] = None
    year_low: Optional[float] = None
    market_status: Optional[MarketStatus] = None
    timestamp: datetime
    
    @field_serializer('timestamp')
    def serialize_timestamp(self, dt: datetime) -> str:
        return dt.isoformat()


class StockData(BaseModel):
    """Comprehensive stock data"""
    symbol: str
    name: Optional[str] = None
    exchange: Optional[str] = None
    currency: Optional[str] = None
    quote: StockQuote
    
    # Company information
    sector: Optional[str] = None
    industry: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None
    
    # Financial metrics
    market_cap: Optional[float] = None
    enterprise_value: Optional[float] = None
    trailing_pe: Optional[float] = None
    forward_pe: Optional[float] = None
    peg_ratio: Optional[float] = None
    price_to_book: Optional[float] = None
    price_to_sales: Optional[float] = None
    
    # Dividends
    dividend_rate: Optional[float] = None
    dividend_yield: Optional[float] = None
    
    # Trading info
    beta: Optional[float] = None
    fifty_day_average: Optional[float] = None
    two_hundred_day_average: Optional[float] = None


class StockHistory(BaseModel):
    """Historical stock data"""
    symbol: str
    data_points: List[DataPoint]
    start_date: datetime
    end_date: datetime
    interval: str
    
    @field_serializer('start_date', 'end_date')
    def serialize_dates(self, dt: datetime) -> str:
        return dt.isoformat()
