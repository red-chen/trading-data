"""
Example scripts for using the Trading Data Service
"""

# Example 1: Get stock data via API
def example_stock_api():
    import requests
    
    # Get comprehensive stock data
    response = requests.get("http://localhost:8000/api/v1/stocks/AAPL")
    print("Apple Stock Data:", response.json())
    
    # Get stock quote only
    response = requests.get("http://localhost:8000/api/v1/stocks/AAPL/quote")
    print("Apple Quote:", response.json())
    
    # Get historical data
    response = requests.get(
        "http://localhost:8000/api/v1/stocks/AAPL/history",
        params={"period": "1mo", "interval": "1d"}
    )
    print("Apple History:", response.json())


# Example 2: Get crypto data via API
def example_crypto_api():
    import requests
    
    # Get Bitcoin data
    response = requests.get("http://localhost:8000/api/v1/crypto/BTC")
    print("Bitcoin Data:", response.json())
    
    # Get historical crypto data
    response = requests.get(
        "http://localhost:8000/api/v1/crypto/BTC/history",
        params={"timeframe": "1h", "limit": 24}
    )
    print("Bitcoin 24h History:", response.json())
    
    # List cryptocurrencies
    response = requests.get(
        "http://localhost:8000/api/v1/crypto/list/all",
        params={"limit": 10}
    )
    print("Top 10 Cryptos:", response.json())


# Example 3: Use services directly
def example_direct_service():
    from services import StockService, CryptoService
    
    # Stock service
    stock_data = StockService.get_stock_data("TSLA")
    print(f"Tesla Price: ${stock_data.quote.price}")
    print(f"Market Cap: ${stock_data.market_cap:,.0f}")
    
    # Crypto service
    crypto_service = CryptoService()
    btc_data = crypto_service.get_crypto_data("BTC")
    print(f"Bitcoin Price: ${btc_data.price:,.2f}")
    print(f"24h Change: {btc_data.change_percent_24h:.2f}%")


if __name__ == "__main__":
    print("=" * 60)
    print("Trading Data Service - Usage Examples")
    print("=" * 60)
    print("\nMake sure the API server is running:")
    print("  python main.py --mode api")
    print("\nThen run these examples:")
    print("  python examples.py")
    print("=" * 60)
    
    # Uncomment to run examples:
    # example_stock_api()
    # example_crypto_api()
    # example_direct_service()
