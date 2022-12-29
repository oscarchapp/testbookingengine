from datetime import datetime, timedelta


def get_today_str() -> str:
    return datetime.today().strftime('%Y-%m-%d')


def get_checkout_min_date() -> str:
    min_date = datetime.today() + timedelta(days=1)
    return min_date.strftime("%Y-%m-%d")


def get_checkout_max_date() -> str:
    return datetime.today().replace(month=12, day=31).strftime('%Y-%m-%d')
