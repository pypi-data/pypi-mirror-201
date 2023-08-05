from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from toolbox import database


class Transaction(database.Base):
    __tablename__ = "transaction"

    id: Mapped[int] = mapped_column(primary_key=True)
    date_of_movement: Mapped[datetime]
    description: Mapped[str] = mapped_column(String(30))
    value: Mapped[float]
    origin: Mapped[str] = mapped_column(String(5))
