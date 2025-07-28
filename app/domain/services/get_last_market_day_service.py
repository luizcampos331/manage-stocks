from datetime import datetime, timedelta

import pendulum


def get_last_market_day_service() -> datetime.date:
    now_et = pendulum.now("America/New_York")
    last_day = now_et - timedelta(days=1)

    while last_day.weekday() >= 5:
        last_day -= timedelta(days=1)

    return last_day.date()
