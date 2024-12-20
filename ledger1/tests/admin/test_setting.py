from ledger1.admin import admin

def test_setting_get_many():
    ret: dict = admin.get(param="setting", query=None)

    assert ret["status_code"] == 200
    assert ret["message"] == "ok"

    user: dict = ret["data"][0]
    assert user == {
        "key": "field_date_min",
        "value": "2020-01-01"
    }


def test_setting_get_filtered():
    ret: dict = admin.get(param="setting", query={'key': ['field_date']})

    assert ret["status_code"] == 200
    assert ret["message"] == "ok"

    data: dict = ret["data"]
    assert data == [
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
    ret: dict = admin.get(param="setting", query=None, record_id="field_date_min")

    assert ret["status_code"] == 200
    assert ret["message"] == "ok"

    data: dict = ret["data"]
    assert data == {
            "key": "field_date_min",
            "value": "2020-01-01"
        }
