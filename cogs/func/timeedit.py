from datetime import timezone, timedelta, datetime

ICT = timezone(timedelta(hours=7))
DAYWEEK_DAY_IN_YEAR = '%a %b %d %Y'
HOUR = '%H:%M'
DAY = '%d/%m'
DAY_HOUR = f'{DAY} {HOUR}'

def to_ict(msg_time, to_string=None):
    msg_time = msg_time.replace(tzinfo=timezone.utc).astimezone(ICT)
    if to_string:
        msg_time = msg_time.strftime(to_string)
    return msg_time

def is_today(msg_time):
    if msg_time.tzinfo != ICT:
        msg_time = to_ict(msg_time)
    return msg_time.date() == datetime.today().date()