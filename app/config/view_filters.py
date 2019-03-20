# Code from https://stackoverflow.com/a/34832184/194964

import pytz
from pytz import timezone

def datetimefilter(value, format="%d/%m/%Y %I:%M %p"):
    tz = pytz.timezone('Australia/Sydney')
    utc = pytz.timezone('UTC')
    value = utc.localize(value, is_dst=None).astimezone(pytz.utc)
    local_dt = value.astimezone(tz)
    return local_dt.strftime(format)

def init_app(app):
    app.jinja_env.filters['datetimefilter'] = datetimefilter
