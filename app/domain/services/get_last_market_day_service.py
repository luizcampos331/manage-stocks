from datetime import datetime, timedelta

import pendulum


def get_last_market_day_service() -> datetime.date:
    now_et = pendulum.now("America/New_York")

    weekday = now_et.weekday()

    if weekday == 0:
        delta_days = 3
    elif weekday == 6:
        delta_days = 2
    elif weekday == 5:
        delta_days = 1
    else:
        delta_days = 1

    last_market_day = now_et - timedelta(days=delta_days)

    while last_market_day.weekday() >= 5:
        last_market_day -= timedelta(days=1)

    return last_market_day.date()
