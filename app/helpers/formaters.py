import datetime


# private
def parse_date(date):
    return datetime.datetime.strptime(date, "%Y-%m-%d").date()


def coma_to_float(string):
    if string is None:
        return None
    string = string.replace(",", ".")
    try:
        return float(string)
    except Exception:
        return None
