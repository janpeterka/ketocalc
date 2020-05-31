import datetime


# private
def parse_date(date):
    return datetime.datetime.strptime(date, "%Y-%m-%d").date()
