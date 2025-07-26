from dataclasses import dataclass

from app.domain.entities.entity import Entity


@dataclass(kw_only=True)
class StockTransaction(Entity):
    stock_symbol: str
    amount: float

    def to_json(self):
        return {
            "id": self.id,
            "stock_symbol": self.stock_symbol,
            "amount": self.amount,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
