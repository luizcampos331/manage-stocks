from datetime import datetime, time, timedelta

import pendulum


def get_last_market_day_service() -> datetime.date:
    now_et = pendulum.now("America/New_York")

    weekday = now_et.weekday()

    if weekday == 5:
        return (now_et - timedelta(days=1)).date()
    elif weekday == 6:
        return (now_et - timedelta(days=2)).date()

    market_close_et = time(hour=16, minute=0)
    if now_et.time() < market_close_et:
        prev_day = now_et - timedelta(days=1)
        while prev_day.weekday() >= 5:
            prev_day -= timedelta(days=1)
        return prev_day.date()

    return now_et.date()
