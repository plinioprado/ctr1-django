from ctr1.admin import admin

API_KEY: str ="Bearer 2s3d4f-1q2w3e4r5t6y7u8i9o0p"

def test_user_get_many():
    ret: dict = admin.get(
        api_key=API_KEY,
        param="users",
        query=None)

    assert ret["status_code"] == 200
    assert ret["message"] == "ok"

    user: dict = ret["data"][0]
    assert user == {
        'id': '1',
        'name': 'John Doe',
        'role': 'admin',
        'email': 'john.doe@example.com',
        'active': True
    }


# def test_user_get_filtered():
#     ret: dict = admin.get(
#         api_key=API_KEY,
#         param="users",
#         query={'name': ['john']})

#     assert ret["status_code"] == 200
#     assert ret["message"] == "ok"

#     user: dict = ret["data"]
#     assert user == [{
#         'id': '1',
#         'name': 'John Doe',
#         'role': 'admin',
#         'active': True,
#     }]


def test_user_get_one():
    ret: dict = admin.get(
        api_key=API_KEY,
        param="users",
        query=None,
        record_id="1")

    assert ret["status_code"] == 200
    assert ret["message"] == "ok"

    user: dict = ret["data"]
    assert user == {
        'id': '1',
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'password': '************',
        "expires": '2030-01-01',
        'role': 'admin',
        'active': True,
    }


def test_user_get_new():
    """ needed by create user requirement"""

    ret: dict = admin.get(
        api_key=API_KEY,
        param="users",
        query=None,
        record_id="new")

    assert ret["status_code"] == 200
    assert ret["message"] == "ok"

    user: dict = ret["data"]
    assert user == {
        'id': 'new',
        'name': '',
        'email': '',
        'expires': '',
        'password': '',
        'role': 'user',
        'active': True,
    }


def test_create_user():

    ret = admin.post(
        api_key=API_KEY,
        param="users",
        data={
            "name": "Alex Doe",
            "email": "alex.doe@example.com",
            "password": "12345",
            "expires": "2030-01-01",
            "role": "users",
            "active": False
        })

    assert ret["status_code"] == 200
    assert ret["message"] == "user 3 created"
    assert ret["data"]["id"] == "3"


def test_update_user():

    ret = admin.put(
        api_key=API_KEY,
        param="users",
        data={
            "id": 3,
            "name": "Alex Doex",
            "email": "alex.doe@example.com",
            "password": "12345",
            "expires": "2030-01-02",
            "role": "users",
            "active": True
        })

    assert ret["status_code"] == 200
    assert ret["message"] == "user 3 updated"
    assert ret["data"]["id"] == "3"


def test_user_delete():

    ret: dict =admin.delete(
        api_key=API_KEY,
        param="users",
        record_id="3")

    assert ret["status_code"] == 200
    assert ret["message"] == "user 3 deleted"
    assert ret["data"]["id"] == "3"
