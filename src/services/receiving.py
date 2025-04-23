# -*- coding: utf-8 -*-
# Глобальные пакеты
import sys
from pyrogram import Client, filters

# Локальные пакеты
from src.data.creds import profiles
from src.config import path

receiver = 'two'
destination = 'one'


api_id = profiles[receiver]['api_id']
api_hash = profiles[receiver]['api_hash']
phone_number = profiles[receiver]['phone']

destination_name = profiles[destination]['nickname']

# Создаем клиент
app = Client(
    name="my_account",
    api_id=api_id,
    api_hash=api_hash,
    phone_number=phone_number,
    workdir=path.sessions_path
)


@app.on_message(filters.private)
async def handle_message(client, message):
    print("\n--- Новое сообщение ---")
    print(f"От: {message.from_user.first_name} (@{message.from_user.username})")
    print(f"Текст: {message.text}")
    print(f"Чат ID: {message.chat.id}")


if __name__ == "__main__":
    print("Бот запущен. Ожидание сообщений... (Ctrl+C для остановки)")
    app.run()
