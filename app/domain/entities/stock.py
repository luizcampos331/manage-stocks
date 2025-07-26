from dataclasses import dataclass

from app.domain.entities.entity import Entity


@dataclass
class Stock(Entity):
    stock_symbol: str
    balance: float

    def to_json(self):
        return {
            "id": self.id,
            "stock_symbol": self.stock_symbol,
            "balance": self.balance,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def increment_balance(self, amount: float):
        self.balance += amount
