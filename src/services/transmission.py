# -*- coding: utf-8 -*-
# Глобальные пакеты
from pyrogram import Client, filters

# Локальные пакеты
from src.data.creds import profiles
from src.config import path


transmiter = 'two'
destination = 'one'


api_id = profiles[transmiter]['api_id']
api_hash = profiles[transmiter]['api_hash']
phone_number = profiles[transmiter]['phone']

destination_name = profiles[destination]['nickname']

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
