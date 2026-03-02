from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.logging import logger
from app.core.middleware import RateLimitMiddleware, RequestLoggingMiddleware, ErrorHandlingMiddleware
from app.db.database import engine, Base
from app.api.v1.router import api_router
from app.api.notifications import router as notifications_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up application...")
    Base.metadata.create_all(bind=engine)
    yield
    logger.info("Shutting down application...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API for 5 Games in a Row - Manchester United Haircut Challenge",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middlewares
app.add_middleware(RateLimitMiddleware, calls=60, period=60)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(ErrorHandlingMiddleware)

# Include routers
app.include_router(api_router, prefix="/api/v1")
app.include_router(notifications_router, prefix="/api/v1/notifications", tags=["Notifications"])


@app.get("/")
async def root():
    return {
        "message": "Welcome to 5 Games in a Row API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": settings.APP_VERSION
    }


@app.get("/info")
async def app_info():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "debug": settings.DEBUG,
    }


if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8002))
    uvicorn.run(app, host="0.0.0.0", port=port)
