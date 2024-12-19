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
    """ post user """


def test_update_user():
    pass


def test_delete_user():
    pass
