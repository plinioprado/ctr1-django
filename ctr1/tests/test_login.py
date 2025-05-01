
import pytest
from ctr1.admin import admin
from ctr1.utils.error_client import ClientError

API_KEY: str ="Bearer 2s3d4f-1q2w3e4r5t6y7u8i9o0p"


def test_login_valid():
    ret: dict = admin.login(data={
        "user_email": "john.doe@example.com",
        "user_pass": "12345",
        "entity": "test"
    })

    assert ret["status_code"] == 200
    assert ret["message"] == "ok"
    assert ret["data"] == {
        "user": {
            "api_key": "2s3d4f-1q2w3e4r5t6y7u8i9o0p",
            "name": "John Doe",
        },
        'menu_options': [
            {
                'key': 'menu_1_text',
                'value': 'Admin',
            },
            {
                'key': 'menu_1-1_text',
                'value': 'Settings',
            },
            {
                'key': 'menu_1-1_path_api',
                'value': '/api/admin/settings',
            },
            {
                'key': 'menu_1-1_path_routing',
                'value': '/admin/settings',
            },
            {
                'key': 'menu_1-2_text',
                'value': 'Users',
            },
            {
                'key': 'menu_1-2_path_api',
                'value': '/api/admin/users',
            },
            {
                'key': 'menu_1-2_path_routing',
                'value': '/admin/users',
            },
        ],
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
            "api_key": "1a2s3d-1q2w3e4r5t6y7u8i9o0p",
            "name": "John Doe",
        },
        "menu_options": [],
        "entity": {
            "name": "Example Ltd.",
        },
    }


def test_login_invalid_data():
    with pytest.raises(ClientError) as err:
        admin.login(data={
            "user_email": "john.doe@example.com",
            "user_pass": "12345",
        })
    assert str(err.value) == "Error: invalid login data"
    assert err.value.status_code == 401


def test_login_invalid_entity():
    with pytest.raises(ClientError) as err:
        admin.login(data={
            "user_email": "john.doe@example.com",
            "user_pass": "12345",
            "entity": "invalid"
        })
    assert str(err.value) == "Error: invalid login"
    assert err.value.status_code == 401



def test_login_invalid_user_or_pass():
    with pytest.raises(ClientError) as err:
        admin.login(data={
            "user_email": "john.doe@example.com",
            "user_pass": "999999",
            "entity": "test"
        })
    assert str(err.value) == "Error: invalid login"
    assert err.value.status_code == 401
