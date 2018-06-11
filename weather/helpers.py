import datetime


def round_date(date):
    result = date.replace(microsecond=0, second=0, minute=0)

    while result.hour % 3 != 0:
        result = result - datetime.timedelta(hours=1)

    return result


def get_intervaks_count(td):
    return (td.total_seconds() / 3600) / 3 + 1


def get_all_dates(from_date, to_date):
    all_dates = []
    date = to_date

    while date >= from_date:
        all_dates.append(date)
        date -= datetime.timedelta(hours=3)

    return all_dates
