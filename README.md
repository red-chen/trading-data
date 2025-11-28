# Trading Data Service

A Python-based service providing stock and cryptocurrency market data through both RESTful API and MCP (Model Context Protocol).

## Features

- 📈 **Stock Data**: Real-time and historical stock market data
- 💰 **Cryptocurrency Data**: Real-time and historical crypto market data
- 🔌 **Dual Protocol Support**:
  - RESTful API (FastAPI)
  - MCP Server (FastMCP) for AI integration

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd trading-data
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Usage

### Start RESTful API Server

```bash
python main.py --mode api
```

The API will be available at `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

### Start MCP Server

```bash
python main.py --mode mcp
```

The MCP server will start at: `http://localhost:8001`
- MCP Endpoint: `http://localhost:8001/mcp`
- Transport: Streamable HTTP

### API Endpoints

#### Stock Data
- `GET /api/v1/stocks/{symbol}` - Get current stock data
- `GET /api/v1/stocks/{symbol}/history` - Get historical stock data
- `GET /api/v1/stocks/{symbol}/quote` - Get stock quote

#### Cryptocurrency Data
- `GET /api/v1/crypto/{symbol}` - Get current crypto data
- `GET /api/v1/crypto/{symbol}/history` - Get historical crypto data
- `GET /api/v1/crypto/list` - List available cryptocurrencies

### MCP Tools

The MCP server (built with FastMCP) provides the following tools via HTTP Streamable transport:
- `get_stock_data` - Retrieve stock market data
- `get_crypto_data` - Retrieve cryptocurrency data
- `get_historical_data` - Get historical price data
- `search_symbols` - Search for stock/crypto symbols

**Connection:**
- Transport: Streamable HTTP
- URL: `http://localhost:8001/mcp/v1`
- Protocol: MCP over Streamable HTTP

## Architecture

```
trading-data/
├── api/                    # RESTful API implementation
│   ├── routers/           # API route handlers
│   └── app.py             # FastAPI application
├── mcp_server/            # MCP server implementation
│   └── server.py          # MCP server
├── models/                # Data models
├── services/              # Data provider services
├── config/                # Configuration
└── main.py               # Entry point
```

## License

MIT License
