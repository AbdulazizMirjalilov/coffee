from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket

from app.api import router
from app.core.config import settings
from app.core.db import async_get_db
from app.models import User
from app.services.chat import chat_endpoint
from app.services.user import get_current_user_ws

APP_NAME = settings.APP_NAME
app = FastAPI(title=APP_NAME, version=settings.APP_VERSION)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.websocket("/ws/chat")
async def websocket_chat(
    websocket: WebSocket,
    db: AsyncSession = Depends(async_get_db),
    user: User = Depends(get_current_user_ws),
):
    await chat_endpoint(websocket, db, user)


@app.get("/", include_in_schema=False)
async def root():
    return {"message": f"{APP_NAME} is running"}


@app.get("/health_check")
async def health_check():
    return {"status": "ok"}
