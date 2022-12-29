from datetime import datetime, timedelta


def get_today_str() -> str:
    """
    Returns today date string in %Y-%m-%d format
    """
    return datetime.today().strftime('%Y-%m-%d')


def get_checkout_min_date() -> str:
    """
    Returns the min date string for the checkout in %Y-%m-%d format
    """
    min_date = datetime.today() + timedelta(days=1)
    return min_date.strftime("%Y-%m-%d")


def get_checkout_max_date() -> str:
    """
    Returns the max date string for the checkout in %Y-%m-%d format
    """
    return datetime.today().replace(month=12, day=31).strftime('%Y-%m-%d')
