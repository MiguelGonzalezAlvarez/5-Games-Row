from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Set
from app.db.database import get_db
from app.models.models import User
from app.core.security import decode_token
import json
import asyncio

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {
            "match_updates": set(),
            "challenge_updates": set(),
            "standings_updates": set(),
        }
        self.user_sockets: Dict[WebSocket, int] = {}

    async def connect(self, websocket: WebSocket, channel: str):
        await websocket.accept()
        if channel not in self.active_connections:
            self.active_connections[channel] = set()
        self.active_connections[channel].add(websocket)

    def disconnect(self, websocket: WebSocket):
        for channel in self.active_connections:
            self.active_connections[channel].discard(websocket)
        if websocket in self.user_sockets:
            del self.user_sockets[websocket]

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        try:
            await websocket.send_json(message)
        except Exception:
            pass

    async def broadcast(self, message: dict, channel: str):
        if channel in self.active_connections:
            disconnected = set()
            for connection in self.active_connections[channel]:
                try:
                    await connection.send_json(message)
                except Exception:
                    disconnected.add(connection)
            for conn in disconnected:
                self.disconnect(conn)

    def get_channel_count(self, channel: str) -> int:
        return len(self.active_connections.get(channel, set()))


manager = ConnectionManager()


async def get_current_user_websocket(websocket: WebSocket) -> int:
    try:
        token = websocket.query_params.get("token")
        if not token:
            return None
        payload = decode_token(token)
        return payload.get("sub")
    except Exception:
        return None


@router.websocket("/ws/{channel}")
async def websocket_endpoint(
    websocket: WebSocket, 
    channel: str,
    user_id: int = Depends(get_current_user_websocket)
):
    await manager.connect(websocket, channel)
    if user_id:
        manager.user_sockets[websocket] = user_id

    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                if message.get("type") == "ping":
                    await manager.send_personal_message({"type": "pong"}, websocket)
            except json.JSONDecodeError:
                pass
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@router.websocket("/ws")
async def websocket_default(websocket: WebSocket):
    await manager.connect(websocket, "general")


async def notify_match_update(match_data: dict):
    await manager.broadcast({
        "type": "match_update",
        "data": match_data
    }, "match_updates")


async def notify_challenge_update(challenge_data: dict):
    await manager.broadcast({
        "type": "challenge_update",
        "data": challenge_data
    }, "challenge_updates")


async def notify_standings_update(standings_data: dict):
    await manager.broadcast({
        "type": "standings_update",
        "data": standings_data
    }, "standings_updates")


@router.get("/ws/stats")
async def get_websocket_stats():
    return {
        "match_updates": manager.get_channel_count("match_updates"),
        "challenge_updates": manager.get_channel_count("challenge_updates"),
        "standings_updates": manager.get_channel_count("standings_updates"),
        "total_connections": sum(len(connections) for connections in manager.active_connections.values())
    }
