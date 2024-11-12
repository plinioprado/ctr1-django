import datetime

def date_iso_to_timestamp(date_iso: str) -> int:
    return datetime.datetime.fromisoformat(date_iso).timestamp()

def date_timestamp_to_iso(date_timestamp: int) -> str:
    return datetime.datetime.fromtimestamp(date_timestamp).isoformat()[0:10]
