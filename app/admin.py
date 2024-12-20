from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command


admin = Router()

@admin.message(Command('adminpanel'))
async def cmd_apanel(message: Message):
    await message.answer('Это админ-панель')

@admin.message()
async def echo(message: Message) -> None:
    await message.answer("Это неизвестная команда")