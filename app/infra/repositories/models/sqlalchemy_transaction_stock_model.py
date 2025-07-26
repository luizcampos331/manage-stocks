import datetime
from typing import Optional

from sqlalchemy import DateTime, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infra.database.sqlalchemy_database_config import BaseSqlalchemyDatabaseConfig


class StockTransactionModel(BaseSqlalchemyDatabaseConfig):
    __tablename__ = "stock_transactions"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    stock_symbol: Mapped[str] = mapped_column(String, nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
