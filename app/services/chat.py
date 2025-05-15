from uuid import UUID

from fastapi import Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import async_get_db
from app.models import SupportMessage
from app.models.user import User
from app.services.user import get_current_user_ws

active_connections: dict[UUID, WebSocket] = {}


async def save_message(
    db: AsyncSession, sender_id: UUID, receiver_id: UUID, message: str
):
    msg = SupportMessage(sender_id=sender_id, receiver_id=receiver_id, message=message)
    db.add(msg)
    await db.commit()


async def chat_endpoint(
    websocket: WebSocket,
    db: AsyncSession = Depends(async_get_db),
    current_user: User = Depends(get_current_user_ws),
):
    await websocket.accept()
    active_connections[current_user.id] = websocket

    try:
        while True:
            data = await websocket.receive_json()
            message = data.get("message")
            receiver_id = UUID(data.get("receiver_id"))

            await save_message(db, current_user.id, receiver_id, message)

            receiver_ws = active_connections.get(receiver_id)
            if receiver_ws:
                await receiver_ws.send_json(
                    {"from": str(current_user.id), "message": message}
                )

    except WebSocketDisconnect:
        active_connections.pop(current_user.id, None)
