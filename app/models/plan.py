from datetime import datetime
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Plan(Base):
    __tablename__ = 'plans'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    ticket_list: Mapped[int] = mapped_column(Integer)
    price: Mapped[int] = mapped_column(Integer)