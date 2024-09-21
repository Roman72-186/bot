from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton, 
                           ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove)
from aiogram.utils.keyboard import InlineKeyboardBuilder



def get_callback_btns(*, btns: dict[str, str], sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()

    for text, data in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

    return keyboard.adjust(*sizes).as_markup()

