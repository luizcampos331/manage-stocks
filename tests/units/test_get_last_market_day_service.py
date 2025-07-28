from datetime import date

from freezegun import freeze_time

from app.domain.services.get_last_market_day_service import get_last_market_day_service


@freeze_time("2024-07-29T21:00:00Z")
def test_returns_friday_if_monday():
    assert get_last_market_day_service() == date(2024, 7, 26)


@freeze_time("2024-07-30T10:00:00Z")
def test_returns_monday_if_tuesday():
    assert get_last_market_day_service() == date(2024, 7, 29)


@freeze_time("2024-07-27T14:00:00Z")
def test_returns_friday_if_saturday():
    assert get_last_market_day_service() == date(2024, 7, 26)


@freeze_time("2024-07-28T14:00:00Z")
def test_returns_friday_if_sunday():
    assert get_last_market_day_service() == date(2024, 7, 26)
