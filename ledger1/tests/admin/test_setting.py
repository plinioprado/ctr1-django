from ledger1.admin import admin

admin.reset()

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
    assert ret["message"] == "setting 7 created"
    assert ret["data"] == { "key": "7" }
