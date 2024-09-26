""" pytest unit tests """

from invoice1.invoice1_service import Invoice1Service as service


def test_reset():
    """ Test reset invoice db """

    response = service.reset()
    assert isinstance(response, dict)
    assert response == {
        "code":200,
        "message": "invoice reset"
    }


def test_get():
    """ Test read all invoices """

    response = service.get()
    assert isinstance(response, dict)
    assert response == {
        "code": 200,
        "message": "ok",
        "data": [
            {
                "num": 1,
                "value": 1000.00,
                "issue_date": "2020-01-15",
                "parts_seller_name": "Example Ltd",
                "parts_buyer_name": "Cedar stores Ltd.",
                "status": "open"
            },
            {
                "num": 2,
                "value": 1200.00,
                "issue_date": "2020-01-16",
                "parts_seller_name": "Example Ltd",
                "parts_buyer_name": "Mahogany Manufacturing Ltd.",
                "status": "open"
            }]
        }


def test_get_by_num():
    """ Test read one invoice """

    response = service.get_by_num(2)
    assert isinstance(response, dict)
    assert response == {
        "code": 200,
        "message": "ok",
        "data": {
                "num": 2,
                "value": 1200.00,
                "issue_date": "2020-01-16",
                "parts_seller_name": "Example Ltd",
                "parts_buyer_name": "Mahogany Manufacturing Ltd.",
                "status": "open"
            }
        }


def test_post():
    """ Test create/post invoice """

    response = service.post({
        "value": 1100.00,
        "issue_date": "2020-01-02",
        "parts_seller_name": "Example Ltd",
        "parts_buyer_name": "Cedar Stores Ltd.",
        "status": "open"
    })
    assert isinstance(response, dict)
    assert response == {
        "code": 200,
        "message": "invoice 3 created"
    }

    response = service.get_by_num(3)
    assert response == {
        "code": 200,
        "message": "ok",
        "data": {
            "num": 3,
            "value": 1100.00,
            "issue_date": "2020-01-02",
            "parts_seller_name": "Example Ltd",
            "parts_buyer_name": "Cedar Stores Ltd.",
            "status": "open"
        }
    }


def test_put():
    """ Test update/put invoice """

    response = service.put({
        "num": 3,
        "value": 1100.00,
        "issue_date": "2020-01-02",
        "parts_seller_name": "Example Ltd",
        "parts_buyer_name": "Cedar Stores Ltd.",
        "status": "open"
    })
    assert isinstance(response, dict)
    assert response == {
        "code": 200,
        "message": "invoice 3 updated"
    }

    response = service.get_by_num(3)
    assert response == {
        "code": 200,
        "message": "ok",
        "data": {
            "num": 3,
            "value": 1100.00,
            "issue_date": "2020-01-02",
            "parts_seller_name": "Example Ltd",
            "parts_buyer_name": "Cedar Stores Ltd.",
            "status": "open"
        }
    }


def test_delete():
    """ Test delete invoice """

    response = service.delete({"num": 3})
    assert isinstance(response, dict)
    assert response == {
        "code": 200,
        "message": "invoice 3 deleted"
    }
    response = service.get_by_num(3)
    assert response == {
        "code": 200,
        "message": "ok",
        "data": {}
    }
