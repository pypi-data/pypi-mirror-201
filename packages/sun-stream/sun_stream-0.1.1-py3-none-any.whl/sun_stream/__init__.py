"""Generates a sequence of sun-rise and sun-set actions

Example:

```python
# Announcing the sun-rises and sun-sets at Mt. Everest:
for action in sun_stream(27.986065, 86.922623, include_now=False):
    if action == SunAction.RISE:
        print("Sun rises at Mt. Everest")
    else:
        print("Sun sets at Mt. Everest")
```

To set desktop colorscheme according to diurnal pattern in Plasma:

```
for action in sun_stream(27.986065, 86.922623, include_now=True):
    if action == SunAction.RISE:
        subprocess.run(["plasma-apply-colorscheme", "BreezeLight"])
    else:
        subprocess.run(["plasma-apply-colorscheme", "BreezeDark"])
```

In this example, having `include_now` being `True` provides a little
convenience, that the iterable yields immediately the current state of
the sun (or the latest rise/set action before now), so the program takes
effect setting the appropriate theme first thing after launching, instead
of waiting for the next event to happen.

"""

from datetime import datetime
import time
from typing import Iterable
import requests
import enum


__all__ = ["SunAction", "sun_stream"]


class SunAction(enum.Enum):
    """Two actions of the sun: RISE and SET."""

    RISE = enum.auto()
    SET = enum.auto()


def sun_stream(
    latitude: float, longitude: float, include_now: bool = True
) -> Iterable[SunAction]:
    """Yield a sequence of sun-rise and sun-set actions at the time it happens

    This function fetches the time of the solar pattern from
    <https://sunrise-sunset.org/>, and will only issue requests when needed.

    If `include_now` is set to `True`, the state of _now_ is instantly yielded. For
    example, if the current moment is midnight, the first action would be
    ``SunAction.SET``; if the current moment is at noon, the first action would be
    ``SunAction.RISE``.

    Args:
        latitude (float): the latitude of the place.
        longitude (float): the longtiude of the place.
        include_now (bool): whether to include the sun's state at the current moment.
            Defaults to ``True``.

    Yields:
        SunAction: The sun's action at the moment.
    """
    now = datetime.now()
    generator = _sun_time_gen(latitude, longitude, now)
    if include_now:
        yield next(generator)[1]
    else:
        next(generator)

    for scheduled_time, action in generator:
        time.sleep(_seconds_until(scheduled_time))
        yield action


def _seconds_until(deadline: datetime) -> float:
    """Returns the length of time from now to deadline, in seconds

    Args:
        deadline (datetime): The instance of time.

    Returns:
        float: Total seconds from now to `deadline`
    """
    now = datetime.now()
    seconds = max(0, (deadline - now).total_seconds())
    return seconds


_URL = "https://api.sunrise-sunset.org/json?lat={latitude}&lng={longitude}"


def _fetch_sun_times(latitude, longitude, date):
    response = requests.get(
        _URL, params={"lat": latitude, "lng": longitude, "date": date, "formatted": "0"}
    ).json()

    sunset = datetime.fromisoformat(response["results"]["sunset"])
    sunrise = datetime.fromisoformat(response["results"]["sunrise"])
    return (sunrise, sunset)


def _sun_time_gen(latitude, longtitude, now: datetime):
    date = now.date()

    sunrise, sunset = _fetch_sun_times(latitude, longtitude, date.isoformat())
    now = now.astimezone(sunrise.tzinfo)
    
    if now < sunrise:
        yield now, SunAction.SET
        yield sunrise, SunAction.RISE
        yield sunset, SunAction.SET
    elif now < sunset:
        yield now, SunAction.RISE
        yield sunset, SunAction.SET
    else:
        yield now, SunAction.SET

    while True:
        date = date + datetime.timedelta(days=1)
        sunrise, sunset = _fetch_sun_times(latitude, longtitude, date.isoformat())
        yield sunrise, SunAction.RISE
        yield sunset, SunAction.SET
