import datetime


def created_recently(item_list, days=30):
    if hasattr(item_list[0], "created_at"):
        attr = "created_at"
    elif hasattr(item_list[0], "created"):
        attr = "created"
    else:
        raise AttributeError

    date_from = datetime.datetime.now() - datetime.timedelta(days=days)

    return [i for i in item_list if (
            hasattr(i, attr)
            and getattr(i, attr) is not None
            and getattr(i, attr) > date_from
        )]


def created_at_date(item_list, date):
    if hasattr(item_list[0], "created_at"):
        attr = "created_at"
    elif hasattr(item_list[0], "created"):
        attr = "created"
    else:
        raise AttributeError

    return [item for item in item_list if (
            hasattr(item, attr)
            and getattr(item, attr) is not None
            and getattr(item, attr).date() == date
        )]
