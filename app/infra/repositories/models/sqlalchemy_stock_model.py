import datetime
from typing import Optional

from sqlalchemy import DateTime, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infra.database.sqlalchemy_database_config import BaseSqlalchemyDatabaseConfig


class StockModel(BaseSqlalchemyDatabaseConfig):
    __tablename__ = "stocks"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    stock_symbol: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    balance: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
