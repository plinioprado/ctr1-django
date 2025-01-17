from ledger1.utils import dateutil


def test_date_iso_to_timestamp():
    # Valid ISO date
    date_iso = "2020-01-01"
    expected_timestamp = 1577865600.0
    print(dateutil.date_iso_to_timestamp(date_iso))
    assert dateutil.date_iso_to_timestamp(date_iso) == expected_timestamp

    # Valid ISO date with time
    try:
        dateutil.date_iso_to_timestamp("2020-01-01T12:00:00")
        assert False, "date with time"
    except ValueError:
        pass

    # Invalid ISO date
    try:
        dateutil.date_iso_to_timestamp("2020-01-32")
        assert False, "Invalid date"
    except ValueError:
        pass

    # Empty string
    try:
        dateutil.date_iso_to_timestamp("")
        assert False, "Empty date"
    except ValueError:
        pass

    # None value
    try:
        dateutil.date_iso_to_timestamp(None)
        assert False, "None date"
    except ValueError:
        pass

def test_date_timestamp_to_iso():

    timestamp = 1577865600  # Corresponds to 2020-01-01
    expected_date = "2020-01-01"
    assert dateutil.date_timestamp_to_iso(timestamp) == expected_date

    # Test with another known timestamp
    timestamp = 1609488000  # Corresponds to 2021-02-01
    expected_date = "2021-01-01"
    assert dateutil.date_timestamp_to_iso(timestamp) == expected_date


def test_date_iso_is_valid():
    # Valid ISO date
    assert dateutil.date_iso_is_valid("2020-01-01") is True

    # Invalid ISO date
    assert dateutil.date_iso_is_valid("2020-01-32") is False

    # Valid ISO date with time
    assert dateutil.date_iso_is_valid("2020-01-01T12:00:00") is True

    # Invalid ISO date with time
    assert dateutil.date_iso_is_valid("2020-01-01T25:00:00") is False

    # Empty string
    assert dateutil.date_iso_is_valid("") is False

    # None value
    assert dateutil.date_iso_is_valid(None) is False
