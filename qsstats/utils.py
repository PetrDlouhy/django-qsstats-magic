import datetime
import re
from dateutil.relativedelta import relativedelta, MO
from qsstats.exceptions import InvalidInterval
from qsstats import compat

def _remove_time(dt):
    tzinfo = getattr(dt, 'tzinfo', compat.now().tzinfo)
    return datetime.datetime(dt.year, dt.month, dt.day, tzinfo=tzinfo)

def _to_datetime(dt):
    if isinstance(dt, datetime.datetime):
        return dt
    return _remove_time(dt)

def _parse_interval(interval):
    num = 1
    match = re.match('(\d+)([A-Za-z]+)', interval)

    if match:
        num = int(match.group(1))
        interval = match.group(2)
    return num, interval

def get_bounds(dt, interval):
    ''' Returns interval bounds the datetime is in. '''

    day = _to_datetime(_remove_time(dt))
    dt = _to_datetime(dt)

    if interval == 'minute':
        begin = datetime.datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, tzinfo=dt.tzinfo)
        end = begin + relativedelta(minutes=1)
    elif interval == 'hour':
        begin = datetime.datetime(dt.year, dt.month, dt.day, dt.hour, tzinfo=dt.tzinfo)
        end = begin + relativedelta(hours=1)
    elif interval == 'day':
        begin = day
        end = day + relativedelta(days=1)
    elif interval == 'week':
        begin = day - relativedelta(weekday=MO(-1))
        end = begin + datetime.timedelta(days=7)
    elif interval == 'month':
        begin = datetime.datetime(dt.year, dt.month, 1, tzinfo=dt.tzinfo)
        end = begin + relativedelta(months=1)
    elif interval == 'year':
        begin = datetime.datetime(dt.year, 1, 1, tzinfo=dt.tzinfo)
        end = datetime.datetime(dt.year+1, 1, 1, tzinfo=dt.tzinfo)
    else:
        raise InvalidInterval('Inverval not supported.')
    end = end - relativedelta(microseconds=1)
    return begin, end
