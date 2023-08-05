import pendulum
from pendulum.tz import local_timezone


def now():
    tz = local_timezone()
    return pendulum.now(tz)
