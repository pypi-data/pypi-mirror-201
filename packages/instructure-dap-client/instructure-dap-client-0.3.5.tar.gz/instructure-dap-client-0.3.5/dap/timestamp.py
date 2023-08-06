from datetime import datetime, timezone


def valid_utc_datetime(s: str) -> datetime:
    """
    Converts a string into a UTC datetime instance.

    :param s: An ISO 8601 timestamp string.
    :returns: A time zone aware datetime instance with time zone UTC.
    """

    # fromisoformat(...) supports military time zone designator "Zulu" to stand for UTC only in Python 3.11 and later
    if s.endswith("Z"):
        # remove time zone suffix "Z" (UTC), parse into naive datetime, and explicitly add time zone designator
        return datetime.fromisoformat(s[:-1]).replace(tzinfo=timezone.utc)
    else:
        # parse as time zone aware datetime directly, and convert to UTC
        return datetime.fromisoformat(s).astimezone(timezone.utc)


def valid_naive_datetime(s: str) -> datetime:
    """
    Converts a string into a naive datetime instance.

    :param s: An ISO 8601 timestamp string.
    :returns: A naive datetime instance that is implicitly assumed to be in time zone UTC.
    """

    # fromisoformat(...) supports military time zone designator "Zulu" to stand for UTC only in Python 3.11 and later
    if s.endswith("Z"):
        # remove time zone suffix "Z" (UTC) and parse into naive datetime
        return datetime.fromisoformat(s[:-1])
    else:
        # parse as time zone aware datetime, convert to UTC, and cast to naive datetime
        return datetime.fromisoformat(s).astimezone(timezone.utc).replace(tzinfo=None)
