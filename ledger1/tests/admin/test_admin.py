from ledger1.admin import admin


def test_reset():
    ret: dict = admin.get(param="reset")

    assert ret["status_code"] == 200
    assert ret["message"] == "reset ok"


def test_login():
    ret: dict = admin.login(data={
        "user_email": "john.doe@example.com",
        "user_pass": "12345",
        "entity": "test"
    })

    assert ret["status_code"] == 200
    assert ret["message"] == "ok"
    assert ret["data"] == {
        "user": {
            "api_key": "2s3d4f1q2w3e4r5t6y7u8i9o0p",
            "name": "John Doe",
        },
        "entity": {
            "name": "Test Ltd.",
        },
    }


def test_login_example():
    ret: dict = admin.login(data={
        "user_email": "john.doe@example.com",
        "user_pass": "12345",
        "entity": "example"
    })

    assert ret["status_code"] == 200
    assert ret["message"] == "ok"
    assert ret["data"] == {
        "user": {
            "api_key": "1a2s3d1q2w3e4r5t6y7u8i9o0p",
            "name": "John Doe",
        },
        "entity": {
            "name": "Example Ltd.",
        },
    }

def test_get_db_settings():
    ret: dict = admin.get_db_settings("field_date")

    assert ret == {
        "field_date_max": "2020-12-31",
        "field_date_min": "2020-01-01"
    }
