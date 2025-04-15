# -*- coding: utf-8 -*-
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pyrogram import Client, filters
import json
from datetime import datetime
import asyncio

from src.config import path
from src.services.сonnectionManager import ConnectionManager
from src.data.creds import profiles

# Инициализация менеджера соединений
manager = ConnectionManager()

# Клиент Telegram
tg_client = Client(
    "my_account",
    api_id=profiles['one']['api_id'],
    api_hash=profiles['one']['api_hash'],
    phone_number=profiles['one']['phone'],
    workdir=path.sessions_path
)

# Глобальная переменная для целевого пользователя
target_user_id = None


async def resolve_target_user():
    """Получаем ID целевого пользователя"""
    global target_user_id
    try:
        user = await tg_client.get_users(profiles['two']['nickname'])
        target_user_id = user.id
        print(f"Target user ID resolved: {target_user_id}")
    except Exception as e:
        print(f"Failed to resolve target user: {e}")
        raise


@tg_client.on_message(filters.private)
async def handle_telegram_message(client, message):
    if message.from_user and message.from_user.id == target_user_id:
        msg_data = {
            "sender": message.from_user.first_name,
            "text": message.text,
            "time": datetime.now().strftime("%H:%M:%S"),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "type": "incoming"
        }
        await manager.broadcast(json.dumps(msg_data))


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Подключаем Telegram клиент
    await tg_client.start()
    print("Telegram client connected")

    # Получаем ID целевого пользователя
    await resolve_target_user()

    yield

    # Отключаем Telegram клиент
    await tg_client.stop()
    print("Telegram client disconnected")


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory=path.static_path), name="static")
templates = Jinja2Templates(directory=path.templates_path)


@app.get("/")
async def get_chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {
        "request": request,
        "target_user": profiles['two']['nickname']
    })


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data == "clear_messages":
                await manager.send_message("clear", websocket)
            elif data.startswith("SEND:"):
                message_text = data[5:]
                await tg_client.send_message(target_user_id, message_text)

                # Эхо-ответ
                msg_data = {
                    "sender": "You",
                    "text": message_text,
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "type": "outgoing"
                }
                await manager.send_message(json.dumps(msg_data), websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("Client disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)
