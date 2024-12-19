from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

main = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Каталог", callback_data="catalog")],
        [
            InlineKeyboardButton(text="Корзина", callback_data="basket"),
            InlineKeyboardButton(text="Контакты", callback_data="contacts"),
        ],
    ]
)

settings = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="YouTube", url="https://youtube.com")]]
)

cars = ["Tesla", "Mercedes", "BMW", "Porche"]


async def inline_cars():
    keyboard = InlineKeyboardBuilder()
    for car in cars:
        keyboard.add(InlineKeyboardButton(text=car, callback_data=f"car_{car}"))
    return keyboard.adjust(2).as_markup()
