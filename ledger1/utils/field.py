""" util pure functions to validate and format generic fields """

import datetime
import math
import re

def date_iso_is_valid(date_iso: str) -> bool:
    try:
        datetime.datetime.fromisoformat(date_iso)

    except ValueError:
        return False

    return True


def date_iso_to_timestamp(date_iso: str) -> int:
    """
    Convert date iso to timestamp through datetime to assure it is valid

    Arguments:
        date_iso (str): date in ISO yyyy-mm-dd

    Returns:
        int: date in unix timestamp
    """

    return math.floor(datetime.datetime.fromisoformat(date_iso).timestamp())


def date_timestamp_to_iso(date_ts: int) -> str:
    """
    Convert date iso to timestamp through datetime to assure it is valid

    Arguments:
        date_iso (str): date in ISO yyyy-mm-dd

    Returns:
        int: date in unix timestamp
    """

    return datetime.datetime.fromtimestamp(date_ts).isoformat()[0:10]


def acc_num_is_valid(acc_num: str) -> bool:
    try:
        if not isinstance(acc_num, str) or not re.match(r"^\d.\d.\d$", acc_num):
            raise ValueError()

    except ValueError:
        return False

    return True
