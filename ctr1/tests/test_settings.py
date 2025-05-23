from ctr1.admin import admin

API_KEY: str ="Bearer 2s3d4f-1q2w3e4r5t6y7u8i9o0p"

def test_setting_get_many():
    ret: dict = admin.get(
        api_key=API_KEY,
        param="settings",
        query=None)

    assert ret["status_code"] == 200
    assert ret["message"] == "ok"
    assert ret["data"][0] == {
        "key": "entity_name",
        "value": "Example Ltd."
    }


def test_setting_get_filtered():
    ret: dict = admin.get(
        api_key=API_KEY,
        param="settings",
        query={'key': ['field_date']})

    assert ret["status_code"] == 200
    assert ret["message"] == "ok"
    assert ret["data"] == [
        {
            "key": "field_date_min",
            "value": "2020-01-01"
        },
        {
            "key": "field_date_max",
            "value": "2020-12-31"
        }
    ]


def test_setting_get_one():
    ret: dict = admin.get(
        api_key=API_KEY,
        param="settings",
        query=None,
        record_id="field_date_min")

    assert ret["status_code"] == 200
    assert ret["message"] == "ok"
    assert ret["data"] == {
        "key": "field_date_min",
        "value": "2020-01-01"
    }


def test_setting_get_new():
    ret: dict = admin.get(
        api_key=API_KEY,
        param="settings",
        query=None,
        record_id="new")

    assert ret["status_code"] == 200
    assert ret["message"] == "ok"
    assert ret["data"] == {
        "key": "",
        "value": ""
    }


def test_seting_create():
    ret = admin.post(
        api_key=API_KEY,
        param="settings",
        data = {
            "key": "test_key",
            "value": "test_value"
        })

    assert ret["status_code"] == 200
    assert ret["message"] == "setting test_key created"
    assert ret["data"] == { "key": "test_key" }


def test_seting_update():
    ret = admin.put(
        api_key=API_KEY,
        param="settings",
        data = {
            "key": "test_key",
            "value": "test_value2"
        })

    assert ret["status_code"] == 200
    assert ret["message"] == "setting test_key updated"
    assert ret["data"] == { "key": "test_key" }


def test_setting_delete():

    ret: dict =admin.delete(
        api_key=API_KEY,
        param="settings",
        record_id="test_id")

    assert ret["status_code"] == 200
    assert ret["message"] == "setting test_id deleted"
    assert ret["data"]["key"] == "test_id"
