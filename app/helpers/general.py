import datetime


def created_recently(item_list, days=30):
    if hasattr(item_list[0], "created_at"):
        attr = "created_at"
    elif hasattr(item_list[0], "created"):
        attr = "created"
    else:
        raise AttributeError

    date_from = datetime.datetime.now() - datetime.timedelta(days=days)

    recent = []
    for i in item_list:
        if (
            hasattr(i, attr)
            and getattr(i, attr) is not None
            and getattr(i, attr) > date_from
        ):
            recent.append(i)
    return recent
