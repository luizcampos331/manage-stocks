import json
from datetime import date, timedelta
from unittest.mock import AsyncMock

import pytest

from app.application.use_cases.get_stock_details_use_case import (
    GetStockDetailsUseCase,
)


@pytest.mark.asyncio
async def test_get_stock_details_use_case_with_cache():
    stock_symbol = "AAPL"
    expected_data = {
        "status": "ok",
        "purchased_amount": 10,
        "purchased_status": "purchased",
        "request_data": str(date.today() - timedelta(days=1)),
        "company_code": stock_symbol,
        "company_name": "Apple Inc",
        "stock_values": {"open": 100, "close": 110},
        "performance_data": {"one_month": 5.5},
        "competitors": [{"name": "MSFT"}],
    }

    mock_cache = AsyncMock()
    mock_cache.get.return_value = json.dumps(expected_data)

    use_case = GetStockDetailsUseCase(
        stock_repository=AsyncMock(),
        stock_values_gateway=AsyncMock(),
        stock_web_scraping_gateway=AsyncMock(),
        cache=mock_cache,
    )

    result = await use_case.execute(stock_symbol)

    assert result == expected_data
    mock_cache.get.assert_awaited_once_with(key=stock_symbol)


@pytest.mark.asyncio
async def test_get_stock_details_use_case_without_cache():
    # Arrange
    stock_symbol = "GOOG"

    mock_cache = AsyncMock()
    mock_cache.get.return_value = None

    mock_stock_repository = AsyncMock()
    mock_stock_repository.find_by_symbol.return_value = type(
        "Stock", (), {"balance": 20}
    )()

    mock_stock_values_gateway = AsyncMock()
    mock_stock_values_gateway.get_by_symbol.return_value = {
        "status": "ok",
        "stock_values": {"open": 150, "close": 160},
    }

    mock_stock_web_scraping_gateway = AsyncMock()
    mock_stock_web_scraping_gateway.scraping_by_symbol.return_value = {
        "company_name": "Google LLC",
        "performance_data": {"one_month": 4.2},
        "competitors": [{"name": "META"}],
    }

    use_case = GetStockDetailsUseCase(
        stock_repository=mock_stock_repository,
        stock_values_gateway=mock_stock_values_gateway,
        stock_web_scraping_gateway=mock_stock_web_scraping_gateway,
        cache=mock_cache,
    )

    result = await use_case.execute(stock_symbol)

    assert result["status"] == "ok"
    assert result["purchased_amount"] == 20
    assert result["purchased_status"] == "purchased"
    assert result["company_code"] == stock_symbol
    assert result["company_name"] == "Google LLC"
    assert result["stock_values"] == {"open": 150, "close": 160}
    assert result["performance_data"] == {"one_month": 4.2}
    assert result["competitors"] == [{"name": "META"}]

    mock_cache.set.assert_awaited_once()
    mock_stock_repository.find_by_symbol.assert_awaited_once_with(stock_symbol)
    mock_stock_values_gateway.get_by_symbol.assert_awaited_once()
    mock_stock_web_scraping_gateway.scraping_by_symbol.assert_awaited_once_with(
        stock_symbol=stock_symbol
    )
