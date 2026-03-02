from fastapi import APIRouter
from app.api.v1 import football, community
from app.api import websocket

api_router = APIRouter()

api_router.include_router(football.router, prefix="/football", tags=["Football"])
api_router.include_router(community.router, prefix="/community", tags=["Community"])
api_router.include_router(websocket.router, prefix="/ws", tags=["WebSocket"])
