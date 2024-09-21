from datetime import datetime
import uuid
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from database.order import Order, UserRole
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

# Добавляем роль
async def orm_add_role(session: AsyncSession, data: dict):
    obj_role = UserRole(
            id_telegram=data["id_telegram"],
            nameRole=data["nameRole"],
            user_name=data["user_name"],
    )
    session.add(obj_role)
    await session.commit()
    
    # Добалвяем заказ
async def orm_add_order(session: AsyncSession, random_id: str, data: dict):
    
    date_obj = datetime.strptime(data["srokOrder"], "%d.%m.%Y").date()
    obj = Order(
            random_id=random_id,
            id_telegram=data["id_telegram"],
            nameOrder=data["nameOrder"],
            fioClienta=data["fioClienta"],
            srokOrder=date_obj,
            discrOrder=data["discrOrder"],
            ispolOrder=data["ispolOrder"],
            status=data.get("status", "Новый заказ")
    )
    session.add(obj)
    await session.commit()
    
    


# Заказы, которые находятся в процессе работы
async def orm_get_orders(session: AsyncSession):
    try:
        async with session.begin():
            result = await session.execute(select(Order).where(Order.status == 'В процессе'))
            orders = result.scalars().all()
            return orders
    except SQLAlchemyError as e:
        (f"Ошибка при получении заказов: {e}")
        return []       
    
    
    
async def orm_get_orders_random(session: AsyncSession, random_id: str):
    try:
        async with session.begin():
            result = await session.execute(select(Order).where(Order.random_id == random_id))
            orders = result.scalars().all()
            return orders
    except SQLAlchemyError as e:
        (f"Ошибка при получении заказов: {e}")
        return [] 
  
    
    
    
    
    
    # Обновление заказа при принятии в работу
async def orm_update_order_accept(session: AsyncSession, random_id: str, ispolOrder: str):
    try:
        # Выполняем запрос на обновление заказа по случайному идентификатору
        query = update(Order).where(Order.random_id == random_id).values(ispolOrder=ispolOrder, status="В работе")
        result = await session.execute(query)  # Выполняем запрос
        await session.commit()  # Сохраняем изменения
        
        return result.rowcount  # Возвращаем количество обновленных строк
    except SQLAlchemyError as e:
        (f"Ошибка при обновлении заказа: {e}")
        await session.rollback()  # Откатываем изменения при ошибке
        return None

      # Обновление заказа при отказе принятия в работу 
async def orm_update_order_reject(session: AsyncSession, random_id: str):
    try:
        # Выполняем запрос на обновление заказа по случайному идентификатору
        query = update(Order).where(Order.random_id == random_id).values(ispolOrder="Не назначено")
        result = await session.execute(query)  # Выполняем запрос
        await session.commit()  # Сохраняем изменения
        
        return result.rowcount  # Возвращаем количество обновленных строк
    except SQLAlchemyError as e:
        (f"Ошибка при обновлении заказа: {e}")
        await session.rollback()  # Откатываем изменения при ошибке
        return None 
    
    # Получение всех заказов, которые не приняты
async def orm_getAll_orders(session: AsyncSession):
    try:
        async with session.begin():
            result = await session.execute(select(Order).where(Order.ispolOrder == 'Не назначено'))
            orders = result.scalars().all()
            return orders
    except SQLAlchemyError as e:
        (f"Ошибка при получении заказов: {e}")
        return []  
    
    
    
async def orm_getAll_role(session: AsyncSession):
    query  = select(UserRole)
    result = await  session.execute(query)
    return result.scalars().all()

# Получение роли по ID TG
async def orm_get_role(session: AsyncSession, id_telegram: int):
    try:
        query = select(UserRole).where(UserRole.id_telegram == id_telegram)
        result = await session.execute(query)
        return result.scalars().first()
    except SQLAlchemyError as e:
        print(f"Ошибка при получении роли: {e}")
        return None

# Получение роли по ID TG
async def orm_get_role_nov(session: AsyncSession, id_tg: int):
    try:
        query = select(UserRole).where(UserRole.id_telegram == id_tg)
        result = await session.execute(query)
        return result.scalars().first()
    except SQLAlchemyError as e:
        print(f"Ошибка при получении роли: {e}")
        return None

# При выборе исполнителя
async def orm_getAll_roles(session: AsyncSession, id_telegram):
    try:
        # Выполняем запрос для получения всех ролей, кроме 'Менеджер'
        query = select(UserRole).where(UserRole.nameRole != 'Менеджер', UserRole.id_telegram != id_telegram)
        result = await session.execute(query)
        roles = result.scalars().all()  # Извлекаем результаты

        # Логируем информацию о полученных ролях
        for role in roles:
             (f"Роль: {role.nameRole}, ID: {role.id_telegram}, Имя: {role.user_name}")

        return roles
    except SQLAlchemyError as e:
        # Логируем ошибку и возвращаем пустой список
        (f"Ошибка при получении ролей: {e}")
        return []

async def assign_executor_to_order(session: AsyncSession, random_id: str, ispolOrder: str):
    """
    Назначает исполнителя к заказу, обновляя соответствующие поля в базе данных.
    
    :param session: Асинхронная сессия базы данных
    :param random_id: Случайный идентификатор заказа
    :param executor_id: ID Telegram выбранного исполнителя
    """
    try:
        # Обновляем заказ, устанавливая исполнителя и изменяя статус на 'Исполнитель назначен'
        query = update(Order).where(Order.random_id == random_id).values(
            ispolOrder=ispolOrder_value,
            status='Исполнитель назначен'
        )
        await session.execute(query)
        await session.commit()
    except SQLAlchemyError as e:
        # Логируем ошибку и откатываем изменения
        (f'Ошибка при обновлении заказа: {e}')
        await session.rollback()


async def orm_update_order(session: AsyncSession, random_id: str, new_ispolOrder: str):
    """
    Обновляет поле ispolOrder для существующего заказа по random_id.
    
    :param session: Асинхронная сессия базы данных
    :param random_id: Уникальный идентификатор заказа
    :param new_ispolOrder: Новое значение поля ispolOrder
    """
    try:
        # Находим существующий заказ по random_id
        result = await session.execute(
            select(Order).where(Order.random_id == random_id)
        )
        order = result.scalars().first()

        if order:
            order.ispolOrder = new_ispolOrder  # Обновляем поле ispolOrder
            await session.commit()  # Коммитим изменения
            (f"Заказ с random_id {random_id} успешно обновлён.")
            return True
        else:
            (f"Заказ с random_id {random_id} не найден.")
            return False
    except SQLAlchemyError as e:
        await session.rollback()
        (f"Ошибка при обновлении заказа: {e}")
        return False

