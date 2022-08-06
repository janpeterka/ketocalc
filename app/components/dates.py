import datetime


def human_format_date(date):
    if date == datetime.date.today():
        return "dnes"
    elif date == datetime.date.today() + datetime.timedelta(days=-1):
        return "včera"
    elif date == datetime.date.today() + datetime.timedelta(days=1):
        return "zítra"
    else:
        return date.strftime("%d.%m.%Y")
