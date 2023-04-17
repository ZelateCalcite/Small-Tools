def add(
        year: str,
        month: str,
        day: str,
        addition: int
) -> str:
    """
    Count the day after the given date added with given addition, supporting 1900-01-01 ~ 9999-12-31

    :param year: str, YYYY
    :param month: str, MM
    :param day: str, DD
    :param addition: int, date interval
    :return: str, YYYY-MM-DD
    """
    if not (year.isdigit() and month.isdigit() and day.isdigit()) \
            and len(year) != 4 and len(month) != 2 and len(day) != 2:
        print('Wrong Date Input')
    if addition < 0:
        print('Wrong Addition')
    year, month, day = int(year), int(month), int(day)
    while addition > 0:
        addition -= 1
        day += 1
        if month in [1, 3, 5, 7, 8, 10, 12] and day > 31:
            day = 1
            month += 1
        pass


def _check_leap_year(
        year: str,
) -> str:
    """
    Check if the year is leap year, supporting 1900 ~ 9999

    :param year: str, YYYY
    :return: str, 'Y':leap year, 'N': not leap year, 'F': wrong input
    """
    if year.isdigit() and 1900 <= int(year) <= 9999:
        year = int(year)
        if year % 100:
            return 'N' if year % 4 else 'T'
        else:
            return 'N' if year % 400 else 'T'
    else:
        return 'F'
