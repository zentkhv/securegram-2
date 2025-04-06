# -*- coding: utf-8 -*-
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pyrogram import Client, filters
import json
from src.data.creds import profiles
from src.config import path

# --- Pyrogram Client Setup ---
tg_client = Client(
    "my_account",
    api_id=profiles['one']['api_id'],
    api_hash=profiles['one']['api_hash'],
    phone_number=profiles['one']['phone'],
    workdir=path.sessions_path
)


# --- WebSocket Manager ---
class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


# --- Telegram Handlers ---
@tg_client.on_message(filters.private)
async def handle_incoming_message(client, message):
    msg_data = {
        "sender": message.from_user.first_name,
        "text": message.text,
        "time": message.date.isoformat()
    }
    await manager.broadcast(f"MSG:{json.dumps(msg_data)}")


# --- Lifespan Manager ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await tg_client.start()
    print("Pyrogram client started")

    yield  # App runs here

    # Shutdown
    await tg_client.stop()
    print("Pyrogram client stopped")


# --- FastAPI App ---
app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory=path.static_path), name="static")
templates = Jinja2Templates(directory=path.templates_path)


# --- Web Routes ---
@app.get("/")
async def chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data.startswith("SEND:"):
                message = data[5:]
                await tg_client.send_message(
                    chat_id=profiles['two']['nickname'],
                    text=message
                )
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        manager.disconnect(websocket)