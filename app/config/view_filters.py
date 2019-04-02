from app.env import SITE_NAME
import pytz

def datetimefilter(value, format="%d/%m/%Y %I:%M %p"):
    # Code from https://stackoverflow.com/a/34832184/194964
    tz = pytz.timezone('Australia/Sydney')
    utc = pytz.timezone('UTC')
    value = utc.localize(value, is_dst=None).astimezone(pytz.utc)
    local_dt = value.astimezone(tz)
    return local_dt.strftime(format)

def site_name(delimiter=''):
    return SITE_NAME + delimiter

def init_app(app):
    app.jinja_env.filters['datetimefilter'] = datetimefilter
    app.jinja_env.filters['site_name'] = site_name
