import datetime

def date_iso_to_timestamp(date_iso: str) -> float:
    return datetime.datetime.fromisoformat(date_iso).timestamp()


def date_timestamp_to_iso(date_timestamp: int) -> str:
    return datetime.datetime.fromtimestamp(date_timestamp).isoformat()[0:10]


def get_date_from(date_iso: str, settings_date: list[dict]):
    date_min_iso = [st for st in settings_date if st["key"].startswith("field_date_min")][0]["value"]

    if date_iso is None:
        return date_min_iso

    date_min_ts = date_iso_to_timestamp(date_min_iso)
    date_ts = date_iso_to_timestamp(date_iso)

    if date_ts < date_min_ts:
        return date_min_iso
    else:
        return date_iso


def get_date_to(date_iso: str, settings_date: dict):
    date_max_iso = [st for st in settings_date if st["key"].startswith("field_date_max")][0]["value"]

    if date_iso is None:
        return date_max_iso

    date_max_ts = date_iso_to_timestamp(date_max_iso)
    date_ts = date_iso_to_timestamp(date_iso)

    if date_ts > date_max_ts:
        return date_max_iso
    else:
        return date_iso
