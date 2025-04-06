# -*- coding: utf-8 -*-
# Глобальные пакеты
import sys
from pyrogram import Client, filters

# Локальные пакеты
from src.data.creds import profiles
from src.config import path


api_id = profiles['one']['api_id']
api_hash = profiles['one']['api_hash']
phone_number = profiles['one']['phone']

destination_name = profiles['two']['nickname']

# Создаем клиент
app = Client(
    name="my_account",
    api_id=api_id,
    api_hash=api_hash,
    phone_number=phone_number,
    workdir=path.sessions_path
)


async def send_message():
    async with app:
        # Отправляем сообщение в личку или чат
        await app.send_message(
            chat_id=destination_name,  # Можно указать @username, +номер или ID чата
            text="Привет! Это тестовое сообщение из Pyrogram!"
        )
        print("Сообщение отправлено!")


if __name__ == "__main__":
    app.run(send_message())
