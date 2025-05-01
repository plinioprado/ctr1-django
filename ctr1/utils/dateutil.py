import re
import datetime


def date_iso_is_valid(date_iso: str) -> bool:

    try:
        if date_iso is None:
            raise ValueError()
        datetime.datetime.fromisoformat(date_iso)

    except ValueError:
        return False

    return True


def date_iso_to_timestamp(date_iso: str) -> float:
    if date_iso is None or re.fullmatch(r'\d{4}-\d{2}-\d{2}?', date_iso) is None:
        raise ValueError(f"Invalid date {date_iso}")

    return float(datetime.datetime.fromisoformat(date_iso).timestamp())


def date_timestamp_to_iso(date_timestamp: int) -> str:
    return datetime.date.fromtimestamp(date_timestamp).isoformat()


def get_date_from(date_iso: str, settings_date: dict):
    date_min_iso = settings_date["field_date_min"]

    if date_iso is None:
        return date_min_iso

    date_min_ts = date_iso_to_timestamp(date_min_iso)
    date_ts = date_iso_to_timestamp(date_iso)

    if date_ts < date_min_ts:
        return date_min_iso
    else:
        return date_iso


def get_date_to(date_iso: str, settings_date: dict):
    date_max_iso = settings_date["field_date_max"]

    if date_iso is None:
        return date_max_iso

    date_max_ts = date_iso_to_timestamp(date_max_iso)
    date_ts = date_iso_to_timestamp(date_iso)

    if date_ts > date_max_ts:
        return date_max_iso
    else:
        return date_iso
