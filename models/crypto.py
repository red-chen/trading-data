from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict, field_serializer
from .common import DataPoint


class CryptoData(BaseModel):
    """Real-time cryptocurrency data"""
    symbol: str
    name: Optional[str] = None
    price: float
    change_24h: float
    change_percent_24h: float
    volume_24h: float
    market_cap: Optional[float] = None
    
    # Price metrics
    high_24h: Optional[float] = None
    low_24h: Optional[float] = None
    ath: Optional[float] = None  # All-time high
    ath_date: Optional[datetime] = None
    atl: Optional[float] = None  # All-time low
    atl_date: Optional[datetime] = None
    
    # Market metrics
    circulating_supply: Optional[float] = None
    total_supply: Optional[float] = None
    max_supply: Optional[float] = None
    
    # Rankings
    market_cap_rank: Optional[int] = None
    
    timestamp: datetime
    
    @field_serializer('timestamp', 'ath_date', 'atl_date')
    def serialize_datetime(self, dt: Optional[datetime]) -> Optional[str]:
        return dt.isoformat() if dt else None


class CryptoHistory(BaseModel):
    """Historical cryptocurrency data"""
    symbol: str
    data_points: List[DataPoint]
    start_date: datetime
    end_date: datetime
    interval: str
    
    @field_serializer('start_date', 'end_date')
    def serialize_dates(self, dt: datetime) -> str:
        return dt.isoformat()


class CryptoListItem(BaseModel):
    """Cryptocurrency list item"""
    symbol: str
    name: str
    market_cap_rank: Optional[int] = None
    price: Optional[float] = None
    market_cap: Optional[float] = None
