from unittest.mock import AsyncMock

import pytest

from app.application.use_cases.register_stock_purchase_use_case import (
    RegisterStockPurchaseInput,
    RegisterStockPurchaseUseCase,
)
from app.domain.entities.stock import Stock


@pytest.mark.asyncio
async def test_register_stock_purchase_with_existing_stock():
    mock_stock_repository = AsyncMock()
    mock_stock_transaction_repository = AsyncMock()
    mock_cache = AsyncMock()

    existing_stock = Stock(stock_symbol="AAPL", balance=10)
    mock_stock_repository.find_by_symbol.return_value = existing_stock

    use_case = RegisterStockPurchaseUseCase(
        stock_repository=mock_stock_repository,
        stock_transaction_repository=mock_stock_transaction_repository,
        cache=mock_cache,
    )

    input_data: RegisterStockPurchaseInput = {
        "stock_symbol": "AAPL",
        "amount": 5,
    }

    result = await use_case.execute(input_data)

    assert result["message"] == "5 units of stock AAPL were added to your stock record"
    assert existing_stock.balance == 15
    mock_stock_repository.update.assert_awaited_once_with(existing_stock)
    mock_stock_transaction_repository.create.assert_awaited_once()
    mock_cache.delete.assert_awaited_once_with(key="AAPL")


@pytest.mark.asyncio
async def test_register_stock_purchase_with_new_stock():
    mock_stock_repository = AsyncMock()
    mock_stock_transaction_repository = AsyncMock()
    mock_cache = AsyncMock()

    mock_stock_repository.find_by_symbol.return_value = None

    use_case = RegisterStockPurchaseUseCase(
        stock_repository=mock_stock_repository,
        stock_transaction_repository=mock_stock_transaction_repository,
        cache=mock_cache,
    )

    input_data: RegisterStockPurchaseInput = {
        "stock_symbol": "GOOG",
        "amount": 20,
    }

    result = await use_case.execute(input_data)

    assert result["message"] == "20 units of stock GOOG were added to your stock record"
    mock_stock_repository.create.assert_awaited_once()
    mock_stock_transaction_repository.create.assert_awaited_once()
    mock_cache.delete.assert_awaited_once_with(key="GOOG")
