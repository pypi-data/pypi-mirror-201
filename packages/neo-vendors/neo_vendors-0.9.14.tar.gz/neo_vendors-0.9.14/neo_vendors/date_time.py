from __future__ import annotations

import datetime
import typing

import pendulum


def utc_now() -> datetime.datetime:
    return pendulum.now(pendulum.UTC)


def date_groups(
        *,
        start_at: datetime.datetime,
        end_at: datetime.datetime,
        max_capacity_days: int,
) -> typing.Iterable[typing.Tuple[datetime.datetime, datetime.datetime]]:
    capacity = datetime.timedelta(days=max_capacity_days)
    interval = int((end_at - start_at) / capacity) + 1
    previous_dt = start_at
    for i in range(interval):
        next_dt = start_at + capacity * (i + 1)
        yield previous_dt, next_dt
        previous_dt = next_dt


def from_pendulum_dt(pend_time: pendulum.DateTime) -> datetime.datetime:
    dt_time = datetime.datetime(
        pend_time.year,
        pend_time.month,
        pend_time.day,
        pend_time.hour,
        pend_time.minute,
        pend_time.second,
        pend_time.microsecond,
    ).astimezone(pend_time.tz)
    return dt_time
