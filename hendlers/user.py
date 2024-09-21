import calendar
from aiogram.enums import ParseMode
from email.utils import parsedate
from json import dumps

import os
import re
import uuid
from aiogram import F, types, Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, or_f, StateFilter
from aiogram.utils.formatting import as_list, as_marked_section, Bold
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton, 
                           ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove)

from aiogram.types import CallbackQuery, Message

from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime
from database.orm_query import assign_executor_to_order, orm_add_order, orm_add_role, orm_get_orders, orm_get_orders_random, orm_get_role, orm_getAll_orders, orm_getAll_role, orm_add_role, orm_getAll_roles, orm_update_order, orm_update_order_accept, orm_update_order_reject

from database.random import generate_unique_id
from keyboards import keyboards

from keyboards.inly_keybords import get_callback_btns
from middlewares.db import DataBaseSession



user_router = Router()

class Role(StatesGroup):
    nameRole = State()
    
class newOrder(StatesGroup):
    nameOrder = State()
    fioClienta = State()
    srokOrder = State()
    discrOrder = State()
    ispolOrder = State()
    
    texts = {
        'newOrder:nameOrder': 'Введите название проекта заново',
        'newOrder:fioClienta': 'Введите ФИО клиента заново',
        'newOrder:srokOrder': 'Введите срок заново',
        'newOrder:discrOrder': 'Введите описание проекта заново',
        'newOrder:ispolOrder': 'Выебрите исполнителя',
    }


@user_router.callback_query(lambda c: c.data == 'start')
async def start_cmd(callback_query: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    id_telegram = callback_query.from_user.id  # Получаем id_telegram от пользователя

    # Получаем роль из базы данных
    role = await orm_get_role(session, id_telegram)
    print(role)
    
    if role is None:
        await callback_query.message.answer('Мы еще не знакомы, давай зарегистрируемся!', reply_markup=keyboards.kb_role)
        await state.set_state(Role.nameRole)
        await callback_query.answer()  # Убираем эффект загрузки на кнопке
        return

    user_role = role.nameRole.lower()  # Приводим роль к нижнему регистру
    keyboard = keyboards.create_story_keyboard(user_role)  # Создаем клавиатуру на основе роли

    # Удаляем инлайн-клавиатуру из предыдущего сообщения
    await callback_query.message.edit_reply_markup(reply_markup=None)

    # Проверяем роли и выводим сообщение с клавиатурой
    if user_role == 'менеджер':
        await callback_query.message.answer(
            '<b>Привет Менеджер!</b>\n\nТы в личном кабинете, где можешь управлять всеми процессами!!!', 
            parse_mode=ParseMode.HTML, 
            reply_markup=keyboard
        )
    elif user_role == 'аранжировщик':
        await callback_query.message.answer(
            '<b>Привет Аранжировщик!</b>\n\nТы в личном кабинете, где можешь управлять всеми процессами!!!', 
            parse_mode=ParseMode.HTML, 
            reply_markup=keyboard
        )
    elif user_role == 'гитарист':
        await callback_query.message.answer(
            '<b>Привет Гитарист!</b>\n\nТы в личном кабинете, где можешь управлять всеми процессами!!!', 
            parse_mode=ParseMode.HTML, 
            reply_markup=keyboard
        )
    else:
        await callback_query.message.answer('Неизвестная роль. Пожалуйста, зарегистрируйтесь заново.', reply_markup=keyboards.kb_role)
        await state.set_state(Role.nameRole)

    # Убираем эффект загрузки на кнопке
    await callback_query.answer()
    
     

@user_router.message(CommandStart())
async def start_cmd(message: types.Message, state: FSMContext, session: AsyncSession):
    id_telegram = message.from_user.id  # Получаем id_telegram от пользователя

    # Получаем роль из базы данных
    role = await orm_get_role(session, id_telegram)
    print(role)
    
    if role is None:
        await message.answer('Мы еще не знакомы, давай зарегистрируемся!', reply_markup=keyboards.kb_role)
        await state.set_state(Role.nameRole)
        return

    user_role = role.nameRole.lower()  # Приводим роль к нижнему регистру
    keyboard = keyboards.create_story_keyboard(user_role)  # Создаем клавиатуру на основе роли

    # Проверяем роли и выводим сообщение с клавиатурой
    if user_role == 'менеджер':
        await message.answer(
            '<b>Привет Менеджер!</b>\n\nТы в личном кабинете, где можешь управлять всеми процессами!!!', 
            parse_mode=ParseMode.HTML, 
            reply_markup=keyboard
        )
    elif user_role == 'аранжировщик':
        await message.answer(
            '<b>Привет Аранжировщик!</b>\n\nТы в личном кабинете, где можешь управлять всеми процессами!!!', 
            parse_mode=ParseMode.HTML, 
            reply_markup=keyboard
        )
    elif user_role == 'гитарист':
        await message.answer(
            '<b>Привет Гитарист!</b>\n\nТы в личном кабинете, где можешь управлять всеми процессами!!!', 
            parse_mode=ParseMode.HTML, 
            reply_markup=keyboard
        )

    
     
@user_router.message(Role.nameRole, F.text == 'Менеджер')
async def start_role(message: types.Message, state: FSMContext, session: AsyncSession):
    user_name = message.from_user.username  # Получаем имя пользователя
    id_telegram = message.from_user.id      # Получаем Telegram ID
    user_role = message.text                # Получаем роль пользователя
    
    # Обновляем состояние FSM данными пользователя
    await state.update_data(id_telegram=id_telegram, nameRole=user_role, user_name=user_name)
    
    # Создаем клавиатуру на основе роли
    keyboard = keyboards.create_story_keyboard(user_role.lower())
    
    # Получаем данные состояния (FSMContext)
    data = await state.get_data()
    
    # Добавляем роль в базу данных
    await orm_add_role(session, data)
    
    # Отправляем приветственное сообщение и клавиатуру
    await message.answer(
        'Привет Менеджер!\n\nСпасибо за регистрацию!',
        parse_mode=ParseMode.HTML,
        reply_markup=keyboards.del_kb
    )
    await message.reply('Ты в личном кабинете, где можешь управлять всеми процессами!', reply_markup=keyboard)
    # Очищаем состояние FSM
    await state.clear()

@user_router.message(Role.nameRole, F.text == 'Аранжировщик')
async def start_role(message: types.Message, state: FSMContext, session: AsyncSession):
    user_name = message.from_user.username  # Получаем имя пользователя
    id_telegram = message.from_user.id      # Получаем Telegram ID
    user_role = message.text                # Получаем роль пользователя
    
    # Обновляем состояние FSM данными пользователя
    await state.update_data(id_telegram=id_telegram, nameRole=user_role, user_name=user_name)
    
    # Создаем клавиатуру на основе роли
    keyboard = keyboards.create_story_keyboard(user_role.lower())
    
    # Получаем данные состояния (FSMContext)
    data = await state.get_data()
    
    # Добавляем роль в базу данных
    await orm_add_role(session, data)
    
    # Отправляем приветственное сообщение и клавиатуру
    await message.answer(
        'Привет Аранжировщик!!!\n\nСпасибо за регистрацию!',
        parse_mode=ParseMode.HTML,
        reply_markup=keyboards.del_kb
    )
    
    await message.reply('Ты в личном кабинете, где можешь управлять всеми процессами!', reply_markup=keyboard)
    
    # Очищаем состояние FSM
    await state.clear()  

@user_router.message(Role.nameRole, F.text == 'Гитарист')
async def start_role(message: types.Message, state: FSMContext, session: AsyncSession):
    user_name = message.from_user.username  # Получаем имя пользователя
    id_telegram = message.from_user.id      # Получаем Telegram ID
    user_role = message.text                # Получаем роль пользователя
    
    # Обновляем состояние FSM данными пользователя
    await state.update_data(id_telegram=id_telegram, nameRole=user_role, user_name=user_name)
    
    # Создаем клавиатуру на основе роли
    keyboard = keyboards.create_story_keyboard(user_role.lower())
    
    # Получаем данные состояния (FSMContext)
    data = await state.get_data()
    
    # Добавляем роль в базу данных
    await orm_add_role(session, data)
    
    # Отправляем приветственное сообщение и клавиатуру
    await message.answer(
        'Привет Гитарист!\n\nСпасибо за регистрацию!',
        parse_mode=ParseMode.HTML,
        reply_markup=keyboards.del_kb
    )
    await message.reply('Ты в личном кабинете, где можешь управлять всеми процессами!', reply_markup=keyboard)
    # Очищаем состояние FSM
    await state.clear()   
    


# FSM
# Новый заказ

@user_router.callback_query(lambda c: c.data == 'neworder')
async def cmd_nameOrder(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession):
    # Ответ на запрос колбэка
    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.answer()
    # Отправляем сообщение с клавиатурой
    await callback_query.message.answer(f'Ты на этапе создания нового проекта.\nУкажи название проекта 👇', reply_markup=keyboards.del_kb)
    await state.set_state(newOrder.nameOrder)

@user_router.message(Command('neworder'))
async def cmd_nameOrder(message: types.Message, state: FSMContext):
    await message.answer(f'Ты на этапе создания нового проекта.\nУкажи название проекта 👇', reply_markup=keyboards.del_kb)
    await state.set_state(newOrder.nameOrder)
    
    
    
@user_router.message(StateFilter('*'), Command('сбросить ввод'))
@user_router.message(StateFilter('*'), F.text.casefold() == "сбросить ввод")
async def cmd_clear(message: types.Message, state: FSMContext) -> None:

        current_state = await state.get_state()
        if current_state is None:
            return
        
        await state.clear()
        await message.answer('Данные сброшены!\nУкажи название проекта 👇', reply_markup=keyboards.del_kb)
        await state.set_state(newOrder.nameOrder)
        
@user_router.message(StateFilter('*'), Command('назад'))
@user_router.message(StateFilter('*'), F.text.casefold() == "назад")
async def cmd_cancel(message: types.Message, state: FSMContext) -> None:
    
    current_state = await state.get_state()
    
    if current_state == newOrder.nameOrder:
        await message.answer('Предыдущего шага нет, введи название проекта!')
        return
    
    previous = None
    for step in newOrder.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f'Ты вернулся к предыдущему шагу!\n {newOrder.texts[previous.state]}', reply_markup=keyboards.kb_order)
            return
        previous = step
        
        
    
@user_router.message(newOrder.nameOrder, F.text)
async def cmd_fioClienta(message: types.Message, state: FSMContext):
    await state.update_data(id_telegram = message.from_user.id)
    await state.update_data(nameOrder = message.text)
    await message.answer(f'Укажи ФИО клиента', reply_markup=keyboards.kb_order)
    await state.set_state(newOrder.fioClienta)
  
@user_router.message(newOrder.nameOrder)
async def cmd_fioClienta(message: types.Message, state: FSMContext):
    await message.answer('Ты вводишь недопустимое значение, данные должны быть в текстовом формате!')

    




@user_router.message(newOrder.fioClienta, F.text)
async def cmd_srokOrder(message: types.Message, state: FSMContext):
    await state.update_data(fioClienta=message.text)
    await message.answer('Укажи срок (в формате 01.01.1970)', reply_markup=keyboards.kb_order)
    await state.set_state(newOrder.srokOrder)

@user_router.message(newOrder.srokOrder, F.text)
async def cmd_srokOrder(message: types.Message, state: FSMContext):
    date_text = message.text
    date_pattern = r'\d{2}\.\d{2}\.\d{4}'
    
    if re.fullmatch(date_pattern, date_text):
        try:
            day, month, year = map(int, date_text.split('.'))
            
            if year > 2050:
                await message.answer('Год не может быть позже 2050. Пожалуйста, укажи правильную дату в формате 01.01.1970.')
            elif month > 12:
                await message.answer('Месяц не может быть больше 12. Пожалуйста, укажи правильную дату в формате 01.01.1970.')
            elif day > 31:
                await message.answer('День не может быть больше 31. Пожалуйста, укажи правильную дату в формате 01.01.1970.')
            else:
                _, last_day = calendar.monthrange(year, month)
                
                if day > last_day:
                    await message.answer(f'В {month:02d} месяце нет {day} дня. Пожалуйста, укажи правильную дату в формате 01.01.1970.')
                else:
                    entered_date = datetime(year, month, day)
                    current_date = datetime.now().date()
                    
                    if entered_date.date() < current_date:
                        await message.answer('Дата не может быть ранее текущего дня. Пожалуйста, укажи правильную дату в формате 01.01.1970.')
                    else:
                        await state.update_data(srokOrder=date_text)
                        await message.answer('Укажи описание проекта', reply_markup=keyboards.kb_order)
                        await state.set_state(newOrder.discrOrder)
        except ValueError:
            await message.answer('Дата не существует. Пожалуйста, укажи правильную дату в формате 01.01.1970.')
    else:
        await message.answer('Ты вводишь недопустимое значение, данные должны быть в формате 01.01.1970!')

    
    
    
@user_router.message(newOrder.discrOrder, F.text)
async def cmd_role(message: types.Message, state: FSMContext, session: AsyncSession):
    id_telegram = message.from_user.id 
    await state.update_data(discrOrder=message.text)
    roles = await orm_getAll_roles(session, id_telegram)  # Получаем все роли, кроме 'Менеджер'
    
    if not roles:
        await message.answer('Нет доступных ролей.')
        return

    # Отправляем информацию о каждой роли с кнопками
    for role in roles:
        role_info = (f'Роль: {role.nameRole}\n'
                    f'ID: {role.id_telegram}\n'
                    f'Имя: {role.user_name}\n')
        await message.answer(
            role_info,
            reply_markup=get_callback_btns(btns={'Выбрать': f'oter_{role.id_telegram}'})
        )

    await message.answer('Выберите исполнителя из доступных 👆')
    
    
    
    
    
@user_router.callback_query(lambda c: c.data.startswith('vibor_ispol_'))
async def cmd_role(callback_query: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    # Подтверждаем получение callback_query без отображения уведомления пользователю
    await callback_query.answer()
    
    try:
        # Разбиваем callback_data по нижнему подчеркиванию
        parts = callback_query.data.split('_')

        # Проверяем, что callback_data имеет ожидаемый формат
        if len(parts) != 3:
            raise ValueError("Некорректный формат callback_data")

        # Извлекаем random_id
        random_id = parts[2]
               
        

    except (IndexError, ValueError) as e:
        # Логируем ошибку для отладки
        await callback_query.message.answer('Ошибка обработки запроса.')
        return

    # Извлекаем ID пользователя, инициировавшего callback_query
    id_telegram = callback_query.from_user.id 

    # Получаем все роли, кроме 'Менеджер'
    roles = await orm_getAll_roles(session, id_telegram)  
    
    if not roles:
        await callback_query.message.answer('Нет доступных ролей.')
        return

    # Отправляем информацию о каждой роли с кнопками
    for role in roles:
        role_info = (
            f'Роль: {role.nameRole}\n'
            f'ID Telegram: {role.id_telegram}\n'
            f'Имя: {role.user_name}\n'
        )
        # Создаём инлайн-клавиатуру с кнопкой "Выбрать" и включаем `random_id` в `callback_data`
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Выбрать', callback_data=f'oterIspol_{role.id_telegram}_{random_id}')]
        ])
        await callback_query.message.answer(
            role_info,
            reply_markup=keyboard
        )

    # Уведомляем пользователя о необходимости выбора исполнителя
    await callback_query.message.answer('Выберите исполнителя из доступных 👆')

    # Устанавливаем состояние ожидания выбора исполнителя (если необходимо)
    await state.set_state(AssignExecutorState.waiting_for_executor_selection)




@user_router.callback_query(lambda c: c.data.startswith('oterIspol_'))
async def handle_role_selection(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession):
    """
    Обработчик выбора роли исполнителя.
    
    :param callback_query: Объект CallbackQuery
    :param state: FSMContext для управления состояниями
    :param session: Асинхронная сессия базы данных
    """
    # Подтверждаем получение callback_query без отображения уведомления пользователю
    await callback_query.answer()
    
    try:
        # Разбиваем callback_data по нижнему подчеркиванию
        parts = callback_query.data.split('_')

        # Проверяем, что callback_data имеет ожидаемый формат: 'oterIspol_{id_telegram}_{random_id}'
        if len(parts) != 3:
            raise ValueError("Некорректный формат callback_data")
        
        # Извлекаем id_telegram и random_id
        id_telegram_str = parts[1]
        random_id = parts[2]
        
        # Преобразуем id_telegram в целое число
        try:
            id_telegram = int(id_telegram_str)
        except ValueError:
            raise ValueError("id_telegram должно быть числом")
        
        # logger.info(f"Извлечён id_telegram: {id_telegram}, random_id: {random_id}")
        
        # Получаем заказ по random_id
        orders = await orm_get_orders_random(session, random_id)
        # logger.info(f"Найдено заказов: {len(orders)} для random_id: {random_id}")
        
        if not orders:
            await callback_query.message.answer('Ошибка: заказ не найден.')
            return
        
        # Предполагается, что random_id уникален и возвращает один заказ
        order = orders[0]
        
        # Получаем информацию об исполнителе
        role = await orm_get_role(session, id_telegram)
        if role is None:
            await callback_query.message.answer('Ошибка: исполнитель не найден.')
            return

    except (IndexError, ValueError) as e:
        # Логируем ошибку для отладки
        # logger.error(f"Ошибка при извлечении данных из callback_data: {e}")
        await callback_query.message.answer('Ошибка обработки запроса.')
        return

    # Обновляем данные состояния FSM и устанавливаем новое состояние
    ispol_order_str = f'{role.nameRole} \\ {role.user_name} \\ {role.id_telegram}'
    await state.update_data(ispolOrder=ispol_order_str)
    await state.set_state(AssignExecutorState.waiting_for_executor_selection)
    
    # Извлекаем данные из заказа
    try:
        random_id = order.random_id  # Замените на актуальное поле, если отличается
        nameOrder = order.nameOrder  # Предполагается, что такое поле есть
        fioClienta = order.fioClienta  # Предполагается, что такое поле есть
        srokOrder = order.srokOrder  # Предполагается, что такое поле есть
        discrOrder = order.discrOrder  # Предполагается, что такое поле есть
    except AttributeError as e:
        # logger.error(f"Ошибка доступа к полям заказа: {e}")
        await callback_query.message.answer('Ошибка доступа к данным заказа.')
        return

    # Форматируем сообщение
    confirmation_message = (
        f'Подтвердите новое назначение.\n\n'
        f'Название проекта: {nameOrder}\n'
        f'ФИО клиента: {fioClienta}\n'
        f'Срок выполнения: {srokOrder}\n'
        f'Описание: {discrOrder}\n'
        f'Исполнитель: {ispol_order_str}\n'
    )
    
    # Разделяем строку по символу обратного слэша для извлечения id_telegram
    parts = ispol_order_str.split('\\')

    # Инициализируем переменную id_telegram
    id_telegram = None

    # Проверяем, что получено достаточное количество частей
    if len(parts) >= 3:
        id_telegram = parts[2].strip()  # Удаляем возможные пробелы
        try:
            id_telegram = int(id_telegram)  # Преобразуем в целое число
        except ValueError:
            # Обработка ошибки, если преобразование не удалось
            id_telegram = None
            # logger.error('Ошибка: id_telegram не является числом.')
    else:
        # Обработка ошибки, если формат строки некорректен
        id_telegram = None
        # logger.error('Ошибка: некорректный формат ispolOrder.')

    # Проверяем, успешно ли извлечён id_telegram
    if id_telegram is not None:
        # Отправляем сообщение с запросом на подтверждение
        await callback_query.message.answer(
            confirmation_message, 
            reply_markup=keyboards.kb_itog_2(random_id, id_telegram)  # Убедитесь, что keyboards.kb_itog_2 определена и принимает два параметра
        )
    else:
        # Отправляем сообщение об ошибке, если не удалось извлечь id_telegram
        await callback_query.message.answer('Ошибка: Не удалось обработать данные исполнителя.')
    
    
    
    
    
@user_router.callback_query(lambda c: c.data.startswith('naz_'))
async def handle_role_selection(callback_query: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    
    await callback_query.answer()
    
    try:
        # Разбиваем callback_data по нижнему подчеркиванию
        parts = callback_query.data.split('_')
        
        random_id = parts[1]

        id_telegram = parts[2]
        print(id_telegram)
        
        # Получаем заказ по random_id
        orders = await orm_get_orders_random(session, random_id)
        # logger.info(f"Найдено заказов: {len(orders)} для random_id: {random_id}")
        
        if not orders:
            await callback_query.message.answer('Ошибка: заказ не найден.')
            return
        
        # Предполагается, что random_id уникален и возвращает один заказ
        order = orders[0]
        
       # Извлекаем данные из заказа
        tg_id = order.id_telegram
        random_id = order.random_id  # Замените на актуальное поле, если отличается
        nameOrder = order.nameOrder  # Предполагается, что такое поле есть
        fioClienta = order.fioClienta  # Предполагается, что такое поле есть
        srokOrder = order.srokOrder  # Предполагается, что такое поле есть
        discrOrder = order.discrOrder  # Предполагается, что такое поле есть
    
        
        # Форматируем сообщение
        confirmation_message = (
            f'Подтвердите исполнение.\n\n'
            f'Название проекта: {nameOrder}\n'
            f'ФИО клиента: {fioClienta}\n'
            f'Срок выполнения: {srokOrder}\n'
            f'Описание: {discrOrder}\n'
        )

    except (IndexError, ValueError) as e:
        # Логируем ошибку для отладки
        # logger.error(f"Ошибка при извлечении данных из callback_data: {e}")
        await callback_query.message.answer('Ошибка обработки запроса.')
        return

    # Отправка сообщения с инлайн клавиатуройв
    await send_message(
        chat_id=id_telegram,
        text=confirmation_message,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Отказаться ❌', callback_data=f'reject_{tg_id}_{random_id}'),
            InlineKeyboardButton(text='Принять ✅', callback_data=f'accept_{tg_id}_{random_id}')],
            [InlineKeyboardButton(text='Продлить ♾️', callback_data=f'srok_{tg_id}_{random_id}')
        ]
    ])
    )
    role = await orm_get_role(session, id_telegram = tg_id)

    if role is None:
        await callback_query.message.answer('Роль не найдена. Пожалуйста, зарегистрируйтесь.')
        return

    user_role = role.nameRole.lower()  # Приводим роль к нижнему регистру
    keyboard = keyboards.create_story_keyboard(user_role)  # Создаем клавиатуру на основе роли

    await callback_query.message.answer('Новый исполнитель назначен', reply_markup=keyboards.del_kb)
    await callback_query.message.reply('Продолжай работу', parse_mode=ParseMode.HTML, reply_markup=keyboard)


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    















@user_router.callback_query(lambda c: c.data.startswith('oter_'))
async def handle_role_selection(callback_query: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    id_telegram = int(callback_query.data.split('_')[1])
    role = await orm_get_role(session, id_telegram)
   
    # Обновляем данные состояния FSM и устанавливаем новое состояние
    await state.update_data(ispolOrder=f'{role.nameRole} \ {role.user_name} \ {role.id_telegram}')
    await state.set_state(newOrder.ispolOrder)
    id_tg = int(callback_query.message.from_user.id)
    data = await state.get_data()
    id_telegram = data.get('id_telegram', 'Не указано')
    nameOrder = data.get('nameOrder', 'Не указано')
    fioClienta = data.get('fioClienta', 'Не указано')
    srokOrder = data.get('srokOrder', 'Не указано')
    discrOrder = data.get('discrOrder', 'Не указано')
    ispolOrder = data.get('ispolOrder', 'Не указано')

    # Форматируем сообщение
    confirmation_message = (
        f'Подтвердите новый проект, все ли верно?\n\n'
        f'Название проекта: {nameOrder}\n'
        f'ФИО клиента: {fioClienta}\n'
        f'Срок выполнения: {srokOrder}\n'
        f'Описание: {discrOrder}\n'
        f'Исполнитель: {ispolOrder}\n'
    )
    # Отправляем сообщение с запросом на подтверждение
    await callback_query.message.answer(confirmation_message, 
        reply_markup=keyboards.kb_itog
    )
    
from aiogram import Bot, Dispatcher, types
bot = Bot(token=os.getenv('TOKEN'))

dp = Dispatcher()


async def send_message(chat_id: int, text: str, reply_markup: ReplyKeyboardMarkup):
    await bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup
    )

     
@user_router.message(F.text == "Подтверждаю")
async def itog(message: types.Message, state: FSMContext, session: AsyncSession):
    # id_tg = message.from_user.id
    random_id = generate_unique_id()  # Генерация случайного идентификатора
    
    data = await state.get_data()
    id_telegram = data.get('id_telegram', 'Не указано')
    nameOrder = data.get('nameOrder', 'Не указано')
    fioClienta = data.get('fioClienta', 'Не указано')
    srokOrder = data.get('srokOrder', 'Не указано')
    discrOrder = data.get('discrOrder', 'Не указано')
    ispolOrder = data.get('ispolOrder', 'Не указано')

    # Форматируем сообщение
    confirmation_message = (
        f'Уникальный номер проекта: {random_id}\n\n'
        f'Название проекта: {nameOrder}\n'
        f'Данные клиента: {fioClienta}\n'
        f'Срок выполнения: {srokOrder}\n'
        f'Описание: {discrOrder}\n'
    )

    # Обработка ispolOrder
    ispolOrder = data.get('ispolOrder', 'Не указано')
    ispolOrder = ispolOrder.split('\\')[2]
    ispolOrder = int(ispolOrder)

    # Отправка сообщения с инлайн клавиатуройв
    await send_message(
        chat_id=ispolOrder,
        text=confirmation_message,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Отказаться ❌', callback_data=f'reject_{id_telegram}_{random_id}'),
            InlineKeyboardButton(text='Принять ✅', callback_data=f'accept_{id_telegram}_{random_id}')],
            [InlineKeyboardButton(text='Продлить ♾️', callback_data=f'srok_{id_telegram}_{random_id}')
        ]
    ])
    )

    # Добавляем новый заказ
    await orm_add_order(session, random_id, data)
    await state.clear()
    
    id_telegram = message.from_user.id 
    role = await orm_get_role(session, id_telegram)

    if role is None:
        await message.answer('Роль не найдена. Пожалуйста, зарегистрируйтесь.')
        return

    user_role = role.nameRole.lower()  # Приводим роль к нижнему регистру
    keyboard = keyboards.create_story_keyboard(user_role)  # Создаем клавиатуру на основе роли

    await message.answer('Заказ проекта добавлен в базу данных и направлен выбранному исполнителю!', reply_markup=keyboards.del_kb)
    await message.reply('Продолжай работу', parse_mode=ParseMode.HTML, reply_markup=keyboard)
   
# Напрвляем информацию о заказе выбранному исполнителю
async def send_message_otvet(chat_id: int, text: str, reply_markup: ReplyKeyboardMarkup):
    await bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup
    )

# Отказать
@user_router.callback_query(lambda c: c.data.startswith('reject_'))
async def handle_reject_selection(callback_query: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    # Подтверждаем выбор пользователя в виде pop-up уведомления
    await callback_query.answer('Твой выбор обработан!')

    # Извлекаем id_telegram из данных callback_query (формат reject_{id_telegram}_{random_id})
    try:
        id_telegram_otvet =str(callback_query.data.split('_')[1])  # Парсим id_telegram из данных callback
    except (IndexError, ValueError) as e:
        # Логируем и обрабатываем ошибку, если данные не корректны
        print(f"Ошибка при обработке id_telegram: {e}")
        await callback_query.answer('Ошибка обработки запроса.')
        return

    # Извлекаем random_id (строка, которая не преобразуется в число)
    try:
        random_id = callback_query.data.split('_')[2]  # random_id остается строкой, так как это UUID
    except IndexError as e:
        # Логируем и обрабатываем ошибку, если random_id не найден
        print(f"Ошибка при обработке random_id: {e}")
        await callback_query.answer('Ошибка обработки запроса.')
        return

    # Удаляем инлайн клавиатуру после выбора (отказ от заказа)
    await callback_query.message.edit_reply_markup(reply_markup=None)
    id_telegram = callback_query.from_user.id  # Получаем id_telegram от пользователя

    # Получаем роль из базы данных
    role = await orm_get_role(session, id_telegram)
    
    user_role = role.nameRole.lower()  # Приводим роль к нижнему регистру
    keyboard = keyboards.create_story_keyboard(user_role)  # Создаем клавиатуру на основе роли
    # Отправляем сообщение в чат, откуда пришел запрос
    await callback_query.message.answer('Вы отказались от исполнения нового заказа!', reply_markup=keyboard)
    
    # Получаем имя пользователя из чата, который вызвал callback
    user_name = callback_query.message.chat.username
    
    # Отправляем уведомление пользователю с id_telegram_otvet, уведомляя его об отказе
    await send_message_otvet(
    chat_id=id_telegram_otvet,
    text=f'@{user_name} отказался от выполнения заказа за № {random_id}.\n\nВыберите другого исполнителя',
    reply_markup=keyboards.get_kb_na_AAA(random_id)
)
    
    # Обновляем статус заказа в базе данных, помечая его как отклоненный
    await orm_update_order_reject(session, random_id)


# Принять
@user_router.callback_query(lambda c: c.data.startswith('accept_'))
async def handle_accept_selection(callback_query: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    # Отправляем пользователю уведомление о том, что его выбор обработан
    await callback_query.answer('Твой выбор обработан!')

    # Извлекаем id_telegram из данных callback_query (формат данных: 'accept_{id_telegram}_{random_id}')
    try:
        id_telegram_otvet = int(callback_query.data.split('_')[1])  # Получаем id_telegram пользователя
    except (IndexError, ValueError) as e:
        # Если возникла ошибка при извлечении id_telegram, логируем её и уведомляем пользователя
        print(f"Ошибка при обработке id_telegram: {e}")
        await callback_query.answer('Ошибка обработки запроса.')
        return

    # Извлекаем random_id (уникальный идентификатор заказа)
    try:
        random_id = callback_query.data.split('_')[2]  # random_id остаётся строкой
    except IndexError as e:
        # Если возникла ошибка при извлечении random_id, логируем её и уведомляем пользователя
        print(f"Ошибка при обработке random_id: {e}")
        await callback_query.answer('Ошибка обработки запроса.')
        return

    # Удаляем инлайн-клавиатуру из сообщения после обработки выбора
    await callback_query.message.edit_reply_markup(reply_markup=None)

    id_telegram = callback_query.from_user.id  # Получаем id_telegram от пользователя

    # Получаем роль из базы данных
    role = await orm_get_role(session, id_telegram)
    
    
    ispolOrder = f'{role.nameRole} \\ {role.user_name} \\ {role.id_telegram}'

    roleKb = await orm_get_role(session, id_telegram_otvet)
    user_role = roleKb.nameRole.lower()  # Приводим роль к нижнему регистру
    keyboard = keyboards.create_story_keyboard(user_role)  # Создаем клавиатуру на основе роли
    # Отправляем сообщение в чат, откуда пришёл запрос, информируя пользователя о принятии заказа
    await callback_query.message.answer('Вы приняли заказ на исполнение!', reply_markup=keyboard)

    # Получаем имя пользователя (username) из чата; если отсутствует, используем "без имени"
    user_name = callback_query.message.chat.username or "без имени"  # Проверка на наличие username

    # Отправляем уведомление пользователю с id_telegram о том, что заказ принят
    await send_message_otvet(
        chat_id=id_telegram_otvet,
        text=f'@{user_name} принял заказ на исполнение за № {random_id}!',
        reply_markup=keyboard
    )
    
    # Обновляем статус заказа в базе данных на "В работе" или другой соответствующий статус
    await orm_update_order_accept(session, random_id, ispolOrder)


# Продлить срок
@user_router.callback_query(lambda c: c.data.startswith('srok_'))
async def handle_accept_selection(callback_query: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    # Отправляем пользователю уведомление о том, что его выбор обработан
    await callback_query.answer('Твой выбор обработан!')

    # Извлекаем id_telegram из данных callback_query (формат данных: 'accept_{id_telegram}_{random_id}')
    try:
        id_telegram = int(callback_query.data.split('_')[1])  # Получаем id_telegram пользователя
    except (IndexError, ValueError) as e:
        # Если возникла ошибка при извлечении id_telegram, логируем её и уведомляем пользователя
        print(f"Ошибка при обработке id_telegram: {e}")
        await callback_query.answer('Ошибка обработки запроса.')
        return

    # Извлекаем random_id (уникальный идентификатор заказа)
    try:
        random_id = callback_query.data.split('_')[2]  # random_id остаётся строкой
    except IndexError as e:
        # Если возникла ошибка при извлечении random_id, логируем её и уведомляем пользователя
        print(f"Ошибка при обработке random_id: {e}")
        await callback_query.answer('Ошибка обработки запроса.')
        return

    # Удаляем инлайн-клавиатуру из сообщения после обработки выбора
    await callback_query.message.edit_reply_markup(reply_markup=None)

    # Отправляем сообщение в чат, откуда пришёл запрос, информируя пользователя о принятии заказа
    await callback_query.message.answer('Вы приняли заказ на исполнение!', reply_markup=keyboards.kb_na_AAA)

    # Получаем имя пользователя (username) из чата; если отсутствует, используем "без имени"
    user_name = callback_query.message.chat.username or "без имени"  # Проверка на наличие username

    # Отправляем уведомление пользователю с id_telegram о том, что заказ принят
    await send_message_otvet(
        chat_id=id_telegram,
        text=f'@{user_name} принял заказ на исполнение!',
        reply_markup=keyboards.kb_na_AAA
    )
    
    # Обновляем статус заказа в базе данных на "В работе" или другой соответствующий статус
    await orm_update_order_accept(session, random_id)


# В процессе
@user_router.callback_query(lambda c: c.data == 'process')
async def process_callback(callback_query: CallbackQuery, session: AsyncSession):
    # Ответ на запрос колбэка
    await callback_query.answer()
    
    # Отправляем сообщение с клавиатурой
    await callback_query.message.answer('Здесь проекты, в которых не назначен исполнитель', reply_markup=keyboards.del_kb)
    
    # Обрабатываем запрос к базе данных
    orders = await orm_getAll_orders(session)
    if not orders:
        await callback_query.message.answer('Нет заказов в процессе.')
        return
    
    for order in orders:
        order_info = (f"Название проекта: {order.nameOrder}\n"
                      f"Данные клиента: {order.fioClienta}\n"
                      f"Описание: {order.discrOrder}\n"
                      f"Исполнитель: {order.ispolOrder}\n"
                      f"Срок: {order.srokOrder.strftime('%d.%m.%Y')}\n")
        await callback_query.message.answer(order_info)
        

@user_router.message(Command('process'))
async def handle_process_command(message: types.Message, session: AsyncSession):
    await message.answer(
        'Здесь проекты, которые находятся в процессе работы\n\n'
        'Назначь исполнителя или удали заказ, если он не актуален',
        reply_markup=keyboards.del_kb
    )
    
    # Обрабатываем запрос к базе данных
    orders = await orm_getAll_orders(session)
    
    if not orders:
        await message.answer('Нет заказов в процессе.')
        return
    
    for order in orders:
        order_info = (f"Уникальный номер проекта: {order.random_id}\n\n"
                      f"Название проекта: {order.nameOrder}\n"
                      f"Данные клиента: {order.fioClienta}\n"
                      f"Описание: {order.discrOrder}\n"
                      f"Исполнитель: {order.ispolOrder}\n"
                      f"Срок: {order.srokOrder.strftime('%d.%m.%Y')}\n")
        
        # Используем правильный синтаксис для формирования callback_data
        await message.answer(
            order_info,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text='Назначить', callback_data=f'upd_order_{order.random_id}'),
                    InlineKeyboardButton(text='Удалить', callback_data='del_order')
                ]
            ])
        )




# Уведомления
@user_router.callback_query(lambda c: c.data == 'notifications')
async def notifications_callback(callback_query: CallbackQuery, session: AsyncSession):
    # Ответ на запрос колбэка
    await callback_query.answer()
    
    # Отправляем сообщение с клавиатурой
    await callback_query.message.answer('Посмотри уведомления по заказам, которые необходимо исполнить:', reply_markup=keyboards.del_kb)

@user_router.message(Command('notifications'))
async def cmd_notifications(message: types.Message):
    await message.answer('Посмотри уведомления по заказам, которые необходимо исполнить:', reply_markup=keyboards.del_kb)
    
    
    
    # История
@user_router.callback_query(lambda c: c.data == 'story')
async def story_callback(callback_query: CallbackQuery, session: AsyncSession):
    id_telegram = callback_query.from_user.id 
    role = await orm_get_role(session, id_telegram)

    user_role = role.nameRole.lower()  # Приводим роль к нижнему регистру
    keyboard = keyboards.create_story_keyboard(user_role)  # Создаем клавиатуру на основе роли

    await callback_query.message.answer('Здесь проекты, которые ты выполнил!', parse_mode=ParseMode.HTML, reply_markup=keyboard)
    await callback_query.answer()  # Убираем эффект нажатия

    

@user_router.message(Command('story'))
async def cmd_story(message: types.Message, session: AsyncSession):
    id_telegram = message.from_user.id 
    role = await orm_get_role(session, id_telegram)

    user_role = role.nameRole.lower()  # Приводим роль к нижнему регистру
    keyboard = keyboards.create_story_keyboard(user_role)  # Создаем клавиатуру на основе роли

    await message.answer('Здесь проекты, которые ты выполнил!', parse_mode=ParseMode.HTML, reply_markup=keyboard)



from aiogram.fsm.state import StatesGroup, State

class AssignExecutorState(StatesGroup):
    waiting_for_executor_selection = State()


# @user_router.callback_query(lambda c: c.data.startswith('vibor_ispol_'))
async def cmd_vibor_ispol(callback_query: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    """
    Обрабатывает нажатие на кнопку "Выбрать исполнителя".
    Выводит список доступных исполнителей для назначения к заказу.
    """
    id_telegram = callback_query.from_user.id 

    try:
        # Извлекаем random_id из callback_data
        random_id = callback_query.data.split('_')[2]
    except (IndexError, ValueError) as e:
        print(f"Ошибка при обработке random_id: {e}")
        await callback_query.answer('Ошибка обработки запроса.')
        return

    # Получаем все роли, кроме 'Менеджер' и текущего пользователя
    roles = await orm_getAll_roles(session, id_telegram)
    
    if not roles:
        # Если нет доступных ролей, уведомляем пользователя
        await callback_query.message.answer('Нет доступных ролей.')
        await callback_query.answer()
        return

    # Отправляем информацию о каждой роли с кнопкой "Выбрать"
    for role in roles:
        role_info = (
            f'Роль: {role.nameRole}\n'
            f'ID Telegram: {role.id_telegram}\n'
            f'Имя: {role.user_name}\n'
        )
        # Создаём инлайн-клавиатуру с кнопкой "Выбрать"
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Выбрать', callback_data=f'select_{role.id_telegram}_{random_id}')]
        ])
        await callback_query.message.answer(
            role_info,
            reply_markup=keyboard
        )

    # Уведомляем пользователя о выборе исполнителя
    await callback_query.message.answer('Выберите исполнителя из доступных 👆')

    # Устанавливаем состояние ожидания выбора исполнителя
    await state.set_state(AssignExecutorState.waiting_for_executor_selection)
    await callback_query.answer()



# @user_router.callback_query(lambda c: c.data.startswith('select_'))
# async def handle_role_selection(callback_query: types.CallbackQuery, state: FSMContext, session: AsyncSession):
#     """
#     Обрабатывает выбор исполнителя из списка.
#     Обновляет поле ispolOrder в существующем заказе и уведомляет исполнителя.
#     """
#     # Извлекаем id_telegram выбранного исполнителя из callback_data
#     try:
#         id_telegram = int(callback_query.data.split('_')[1])  # Предполагается, что формат 'select_ispol_{id}'
#     except (IndexError, ValueError):
#         await callback_query.answer('Некорректные данные выбора исполнителя.')
#         return
#     try:
#         random_id = str(callback_query.data.split('_')[2])  
#     except (IndexError, ValueError):
#         await callback_query.answer('Некорректные данные выбора исполнителя.')
#         return
#     # Получаем информацию об исполнителе из базы данных
#     role = await orm_get_role(session, id_telegram)

#     if role is None:
#         # Если исполнитель не найден, уведомляем пользователя
#         await callback_query.answer('Ошибка: исполнитель не найден.')
#         return

#     # Формируем строку для поля ispolOrder
#     ispolOrder_value = f'{role.nameRole} \\ {role.user_name} \\ {role.id_telegram}'

#     # # Получаем данные заказа из состояния FSM
#     # data = await state.get_data()
#     # random_id = data.get('random_id')

#     if not random_id:
#         await callback_query.message.answer('Ошибка: отсутствует идентификатор заказа.')
#         await callback_query.answer()
#         return

#     # Обновляем поле ispolOrder в существующем заказе
#     update_success = await orm_update_order(session, random_id, ispolOrder_value)
#     data = await state.get_data()
#     id_telegram = data.get('id_telegram', 'Не указано')
#     nameOrder = data.get('nameOrder', 'Не указано')
#     fioClienta = data.get('fioClienta', 'Не указано')
#     srokOrder = data.get('srokOrder', 'Не указано')
#     discrOrder = data.get('discrOrder', 'Не указано')
    
#     if update_success:
#         # Формируем сообщение для исполнителя
#         confirmation_message = (
#             f'Уникальный номер проекта: {random_id}\n\n'
#             f'Название проекта: {nameOrder}\n'
#             f'Данные клиента: {fioClienta}\n'
#             f'Срок выполнения: {srokOrder}\n'
#             f'Описание: {discrOrder}\n'
#         )

#         # Создаём инлайн-клавиатуру для исполнителя
#         keyboard = InlineKeyboardMarkup(inline_keyboard=[
#             [
#             InlineKeyboardButton(text='Отказаться ❌', callback_data=f'reject_{id_telegram}_{random_id}'),
#             InlineKeyboardButton(text='Принять ✅', callback_data=f'accept_{id_telegram}_{random_id}')],
#             [InlineKeyboardButton(text='Продлить ♾️', callback_data=f'srok_{id_telegram}_{random_id}')
#         ]
#         ])
  
        
#         # Отправляем сообщение исполнителю с инлайн-клавиатурой
#         await send_message(
#             chat_id=id_telegram,  # Предполагается, что id_telegram хранится в role
#             text=confirmation_message,
#             reply_markup=keyboard
#         )
        
#         # Уведомляем инициатора о назначении исполнителя (опционально)
#         await callback_query.message.answer(f'Исполнитель успешно назначен к проекту с ID: {random_id}.')
#         await callback_query.answer('Исполнитель назначен успешно.')
#     else:
#         # Уведомляем об ошибке при обновлении заказа
#         await callback_query.message.answer('Ошибка: не удалось обновить заказ. Проверьте правильность данных.')
#         await callback_query.answer('Ошибка при обновлении заказа.')

#     # Очищаем состояние FSM
#     await state.clear()



