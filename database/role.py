from sqlalchemy import DateTime, Float, String, Text, func, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import date

class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    
    

class Role(Base):
    __tablename__ = 'role'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_telegram: Mapped[str] = mapped_column(Text, nullable=False)
    user_role: Mapped[str] = mapped_column(Text, nullable=False)