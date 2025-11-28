#!/usr/bin/env python3
"""
Trading Data Service - Main Entry Point

This service provides stock and cryptocurrency market data through:
- RESTful API (FastAPI)
- MCP Server (Model Context Protocol)
"""
import argparse
import sys
import uvicorn
from config import settings


def run_api_server():
    """Run the RESTful API server"""
    print(f"🚀 Starting Trading Data API Server...")
    print(f"📍 Server: http://{settings.api_host}:{settings.api_port}")
    print(f"📚 API Docs: http://{settings.api_host}:{settings.api_port}/docs")
    print(f"📖 ReDoc: http://{settings.api_host}:{settings.api_port}/redoc")
    
    uvicorn.run(
        "api.app:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
        log_level="info"
    )


def run_mcp_server():
    """Run the MCP server"""
    print(f"🚀 Starting Trading Data MCP Server...")
    print(f"📡 MCP Server: {settings.mcp_server_name}")
    print(f"📍 HTTP Server: http://{settings.mcp_host}:{settings.mcp_port}")
    print(f"🔌 MCP Endpoint: http://{settings.mcp_host}:{settings.mcp_port}/mcp/v1")
    print(f"ℹ️  Transport: Streamable HTTP")
    
    from mcp_server.server import run_mcp_http_server
    
    run_mcp_http_server(host=settings.mcp_host, port=settings.mcp_port)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Trading Data Service - Stock and Cryptocurrency Data Provider"
    )
    parser.add_argument(
        "--mode",
        choices=["api", "mcp"],
        default="api",
        help="Server mode: 'api' for RESTful API, 'mcp' for MCP server (default: api)"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("📊 Trading Data Service")
    print("=" * 60)
    
    try:
        if args.mode == "api":
            run_api_server()
        elif args.mode == "mcp":
            run_mcp_server()
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down gracefully...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
