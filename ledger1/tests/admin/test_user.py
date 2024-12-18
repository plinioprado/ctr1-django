from ledger1.admin import admin

def test_user_get_many():
    ret: dict = admin.get(param="user", filters=None)

    print(ret)

    assert ret["status_code"] == 200

