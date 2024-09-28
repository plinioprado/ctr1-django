""" test Account1 model """

# pylint: disable=missing-function-docstring

from dataclasses import asdict
import pytest
from ledger1.models.account1 import Account1


def test_validation():

    acc = Account1(
            num="9.9.9",
            name="test",
            dc=False
        )

    assert asdict(acc) == {
        'num': '9.9.9',
        'name': 'test',
        'dc': False
    }

    with pytest.raises(ValueError) as err:
        Account1(
            num=1,
            name="test",
            dc=True
        )
    assert str(err.value) == "invalid account number"

    with pytest.raises(ValueError) as err:
        Account1(
            num="9.9.9",
            name=1,
            dc=False
        )
    assert str(err.value) == "invalid account name"

    with pytest.raises(ValueError) as err:
        Account1(
            num="9.9.9",
            name="test",
            dc=2
        )
    assert str(err.value) == "invalid account dc"
