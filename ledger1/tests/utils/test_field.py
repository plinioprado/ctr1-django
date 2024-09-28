""" Test Util functions """

import ledger1.utils.field as field

def test_date_iso_is_valid():
    assert field.date_iso_is_valid("2020-01-02")
    assert not field.date_iso_is_valid("2020-02-30")


def test_acc_num_is_valid():
    assert field.acc_num_is_valid("1.1.1")
    assert not field.acc_num_is_valid("1.1.11")
    assert not field.acc_num_is_valid("x.x.x")
