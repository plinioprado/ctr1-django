import pytest
from ledger1.admin import admin
from ledger1.utils.error_client import ClientError

API_KEY: str ="Bearer 2s3d4f-1q2w3e4r5t6y7u8i9o0p"


def test_get_db_settings():
    ret: dict = admin.get_db_settings("field_date")

    assert ret == {
        "field_date_max": "2020-12-31",
        "field_date_min": "2020-01-01"
    }


def test_reset():
    ret: dict = admin.get(
        api_key=API_KEY,
        param="reset")

    assert ret["status_code"] == 200
    assert ret["message"] == "reset ok"


def test_get_param_invalid():
    with pytest.raises(ClientError) as err:
        admin.get(
            api_key=API_KEY,
            param="zzzzz")
    assert str(err.value) == "Error: invalid param zzzzz"
    assert err.value.status_code == 400
