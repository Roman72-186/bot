from sqlalchemy import DateTime, Float, String, Text, func, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import date

import uuid

class Base(DeclarativeBase):
    # status: Mapped[str] = mapped_column('Новый заказ')
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    
    

class Order(Base):
    __tablename__ = 'order'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    random_id = mapped_column(String, unique=True, default=str(uuid.uuid4()))
    id_telegram: Mapped[str] = mapped_column(Text, nullable=False)
    nameOrder: Mapped[str] = mapped_column(String(150), nullable=False)
    fioClienta: Mapped[str] = mapped_column(String(150), nullable=False)
    srokOrder: Mapped[date] = mapped_column(Date)
    discrOrder: Mapped[str] = mapped_column(Text, nullable=False)
    ispolOrder: Mapped[str] = mapped_column(String(150), nullable=False)
    status: Mapped[str] = mapped_column(String, default='Новый заказ')

    photo: Mapped[str] = mapped_column(String(255), nullable=True)  # Поле для ссылки на фотографию
    comment: Mapped[str] = mapped_column(Text, nullable=True)  # Поле для комментария
    notifications: Mapped[str] = mapped_column(Text, nullable=True)
    
class UserRole(Base):
    __tablename__ = 'role'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_telegram: Mapped[str] = mapped_column(Text, nullable=False)
    nameRole: Mapped[str] = mapped_column(Text, nullable=False) 
    user_name: Mapped[str] = mapped_column(Text) 