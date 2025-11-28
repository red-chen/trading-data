from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from api.routers import stocks, crypto


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    
    app = FastAPI(
        title=settings.api_title,
        version=settings.api_version,
        description=settings.api_description,
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(stocks.router, prefix="/api/v1/stocks", tags=["stocks"])
    app.include_router(crypto.router, prefix="/api/v1/crypto", tags=["crypto"])
    
    @app.get("/")
    async def root():
        return {
            "name": settings.api_title,
            "version": settings.api_version,
            "docs": "/docs",
            "status": "running"
        }
    
    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}
    
    return app


app = create_app()
