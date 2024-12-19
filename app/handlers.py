from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext  # нужен для управления состояниями
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

import app.keyboards as kb
from app.middlewares import TestMiddleware

router = Router()  # как своего рода посредник диспетчера

router.message.outer_middleware(TestMiddleware())


# Создаем модель
class Reg(StatesGroup):
    name = State()
    number = State()


# обработчик, который будет ловить команду старт
@router.message(
    CommandStart()
)  # Диспетчер ждет сообщение команду старт, ответит на него
async def cmd_start(message: Message) -> None:
    await message.reply(
        f"Привет! \nТвой ID: {message.from_user.id}\nИмя: {message.from_user.first_name}",
        reply_markup=kb.main,
    )


@router.message(Command("help"))  # помогает фильтровать команды внутри класса
async def cmd_start(message: Message) -> None:
    await message.answer("Это команда /help")


@router.message(F.text == "Как дела?")  # фильтр
async def how_are_you(message: Message) -> None:
    await message.answer("OK!")


@router.message(F.photo)  # фильтр
async def get_photo(message: Message) -> None:
    await message.answer(f"ID фото: {message.photo[-1].file_id}")


@router.message(Command("get_photo"))
async def get_photo(message: Message) -> None:
    await message.answer_photo(
        photo="AgACAgUAAxkBAAMZZ1cDvAdzTXcBS5JqxXOJxabLHGwAApLDMRuuebhWqtnIS7QeHOgBAAMCAAN5AAM2BA",
        caption="Это реклама мурены",
    )


@router.callback_query(F.data == "catalog")
async def catalog(callback: CallbackQuery) -> None:
    await callback.answer("Вы выбрали этот каталог", show_alert=True)  # уведомление
    await callback.message.edit_text("Привет!", reply_markup=await kb.inline_cars())


@router.message(Command("reg"))
async def reg_one(message: Message, state: FSMContext) -> None:
    await state.set_state(Reg.name)
    await message.answer("Введите Ваше имя")


# теперь нужно словить введенное имя
@router.message(Reg.name)
async def reg_two(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(Reg.number)
    await message.answer("Введите номер телефона")


@router.message(Reg.number)
async def two_three(message: Message, state: FSMContext) -> None:
    await state.update_data(number=message.text)
    data = await state.get_data()
    await message.answer(
        f"Спасибо, регистрация завершена.\nИмя: {data['name']}\nНомер: {data['number']}"
    )
    await state.clear()
