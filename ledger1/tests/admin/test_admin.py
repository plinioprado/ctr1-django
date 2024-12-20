from ledger1.admin import admin


def test_reset():
    ret: dict = admin.get(param="reset")

    assert ret["status_code"] == 200
    assert ret["message"] == "reset ok"


def test_login():
    ret: dict = admin.login(data={
        "user_email": "john.doe@example.com",
        "user_pass": "12345",
        "entity": "example"
    })

    assert ret["status_code"] == 200
    assert ret["message"] == "ok"
    assert ret["data"]["user"]["api_key"] == "1q2w3e4r5t6y7u8i9o0p"
