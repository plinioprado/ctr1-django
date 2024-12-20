from ledger1.admin import admin

def test_user_get_many():
    ret: dict = admin.get(param="user", query=None)

    assert ret["status_code"] == 200
    assert ret["message"] == "ok"

    user: dict = ret["data"][0]
    assert user == {
        'id': '1',
        'name': 'John Doe',
        'role': 'admin',
        'entity': 'example',
        'active': True
    }


def test_user_get_filtered():
    ret: dict = admin.get(param="user", query={'name': ['john']})

    assert ret["status_code"] == 200
    assert ret["message"] == "ok"

    user: dict = ret["data"]
    assert user == [{
        'id': '1',
        'name': 'John Doe',
        'role': 'admin',
        'entity': 'example',
        'active': True,
    }]


def test_user_get_one():
    ret: dict = admin.get(param="user", query=None, record_id="1")

    assert ret["status_code"] == 200
    assert ret["message"] == "ok"

    user: dict = ret["data"]
    assert user == {
        'id': '1',
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'password': '************',
        'role': 'admin',
        'entity': 'example',
        'entities': 'example',
        'active': True,
    }


def test_user_get_new():
    """ needed by create user requirement"""

    ret: dict = admin.get(param="user", query=None, record_id="new")

    assert ret["status_code"] == 200
    assert ret["message"] == "ok"

    user: dict = ret["data"]
    assert user == {
        'id': 'new',
        'name': '',
        'email': '',
        'password': '',
        'role': 'user',
        'entity': 'example',
        'entities': 'example',
        'active': True,
    }


def test_create_user():

    ret = admin.post(
        param="user",
        data={
            "name": "Alex Doe",
            "email": "alex.doe@example.com",
            "password": "12345",
            "role": "user",
            "entities": "example",
            "entity": "example",
            "active": False
        })

    assert ret["status_code"] == 200
    assert ret["message"] == "user 3 created"
    assert ret["data"]["id"] == "3"


def test_update_user():

    ret = admin.put(
        param="user",
        data={
            "id": 3,
            "name": "Alex Doex",
            "email": "alex.doe@example.com",
            "password": "12345",
            "role": "user",
            "entities": "example",
            "entity": "example",
            "active": True
        })

    assert ret["status_code"] == 200
    assert ret["message"] == "user 3 updated"
    assert ret["data"]["id"] == "3"


def test_user_delete():

    ret: dict =admin.delete(param="user", record_id="3")

    assert ret["status_code"] == 200
    assert ret["message"] == "user 3 deleted"
    assert ret["data"]["id"] == "3"
