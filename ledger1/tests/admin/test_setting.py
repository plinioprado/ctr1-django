from ledger1.admin import admin


def test_setting_get_many():
    ret: dict = admin.get(param="setting", query=None)

    assert ret["status_code"] == 200
    assert ret["message"] == "ok"
    assert ret["data"][0] == {
        "key": "field_date_min",
        "value": "2020-01-01"
    }


def test_setting_get_filtered():
    ret: dict = admin.get(param="setting", query={'key': ['field_date']})

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
        param="setting",
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
        param="setting",
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
        param="setting",
        data = {
            "key": "test_key",
            "value": "test_value"
        })

    assert ret["status_code"] == 200
    assert ret["message"] == "setting test_key created"
    assert ret["data"] == { "key": "test_key" }


def test_seting_update():
    ret = admin.put(
        param="setting",
        data = {
            "key": "test_key",
            "value": "test_value2"
        })

    assert ret["status_code"] == 200
    assert ret["message"] == "setting test_key updated"
    assert ret["data"] == { "key": "test_key" }


def test_setting_delete():

    ret: dict =admin.delete(param="setting", record_id="test_id")

    assert ret["status_code"] == 200
    assert ret["message"] == "setting test_id deleted"
    assert ret["data"]["key"] == "test_id"
