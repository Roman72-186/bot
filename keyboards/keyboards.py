from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton, 
                           ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove)
from aiogram.utils.keyboard import ReplyKeyboardBuilder



kb_role = ReplyKeyboardMarkup(
    keyboard=[
        [
        KeyboardButton(text='Менеджер')],
        [KeyboardButton(text='Аранжировщик'),
        KeyboardButton(text='Гитарист')
        ]
    ], resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Выбери свою роль 👇'
)

kb_start_git = ReplyKeyboardBuilder()
kb_start_git.add(
        KeyboardButton(text='В процессе'),
        KeyboardButton(text='Уведомления'),
        KeyboardButton(text='История'),
)
kb_start_git.adjust(2, 2)


kb_start = ReplyKeyboardBuilder()
kb_start.attach(kb_start_git)
kb_start.row(KeyboardButton(text='Новый заказ'))

kb_itog = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Подтверждаю')],
        [KeyboardButton(text='Сбросить ввод')
        ]
    ], resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Итог...'
)

def kb_itog_2(random_id: str, id_telegram: int) -> InlineKeyboardMarkup:
    """
    Создаёт инлайн-клавиатуру с динамическим callback_data.
    
    :param random_id: Уникальный идентификатор заказа
    :return: Объект InlineKeyboardMarkup
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Назначить', 
                    callback_data=f'naz_{random_id}_{id_telegram}'
                )
            ]
        ]
    )



# kb_itog_2 = ReplyKeyboardMarkup(
#     keyboard=[
#         [KeyboardButton(text='Назначить')],
#         [KeyboardButton(text='Сбросить ввод')
#         ]
#     ], resize_keyboard=True,
#     one_time_keyboard=True,
#     input_field_placeholder='Итог...'
# )

kb_order = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Назад'),
        KeyboardButton(text='Сбросить ввод')
        ]
    ], resize_keyboard=True,
    one_time_keyboard=True
)





# Удаление клавиатуры
del_kb = ReplyKeyboardRemove()




def get_kb_na_AAA(random_id: str) -> InlineKeyboardMarkup:
    """
    Создаёт инлайн-клавиатуру с динамическим callback_data.
    
    :param random_id: Уникальный идентификатор заказа
    :return: Объект InlineKeyboardMarkup
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Выбрать исполнителя', 
                    callback_data=f'vibor_ispol_{random_id}'
                )
            ],
            [
                InlineKeyboardButton(
                    text='В главное меню', 
                    callback_data='start'
                )
            ]
        ]
    )


kb_na_GGG = InlineKeyboardMarkup(
    inline_keyboard=[
    [InlineKeyboardButton(text='В процессе', callback_data="process"),
    InlineKeyboardButton(text='Уведомления', callback_data="notifications")],
    [InlineKeyboardButton(text='История', callback_data="story")]
])


def create_story_keyboard(user_role: str) -> InlineKeyboardMarkup:
    # Создаем клавиатуру с пустым списком inline_keyboard
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    if user_role == 'менеджер':
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(text='Новый заказ', callback_data="neworder")
        ])
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(text='В процессе', callback_data="process")
        ])
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(text='Уведомления', callback_data="notifications"),
            InlineKeyboardButton(text='История', callback_data="story")
            
        ])
    elif user_role == 'аранжировщик':
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(text='Новый заказ', callback_data="neworder")
        ])
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(text='Уведомления', callback_data="notifications")
        ])
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(text='В процессе', callback_data="process"),
            InlineKeyboardButton(text='История', callback_data="story")
            
        ])
    elif user_role == 'гитарист':
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(text='В процессе', callback_data="process")
        ])
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(text='В обработке', callback_data="in_processing")
        ])
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(text='Уведомления', callback_data="notifications"),
            InlineKeyboardButton(text='История', callback_data="story")
        ])

    return keyboard

