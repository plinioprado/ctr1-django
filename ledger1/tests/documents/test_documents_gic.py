from ledger1.document import documents

API_KEY: str ="Bearer 2s3d4f-1q2w3e4r5t6y7u8i9o0p"

def test_get_many_gic():
    response = documents.get(
        api_key=API_KEY,
        doc_dc=False,
        doc_type="gic",
        doc_num=None)

    assert response["status"] == 200
    assert response["message"] == "wip"
    assert response["data"] == [
        {
            "doc_num": "003.55555.444444444",
            "descr": "GIC",
            "acc_num": "1.1.4"
        }]


def test_get_one_gic():
    response = documents.get(
        api_key=API_KEY,
        doc_dc=False,
        doc_type="gic",
        doc_num="003.55555.444444444")

    assert response["status"] == 200
    assert response["message"] == "ok"
    assert response["data"] == {
        "doc_num": "003.55555.444444444",
        "descr": "GIC",
        "acc_num": "1.1.4",
        "fields": {
            "detail": {
                "anticipated_interest": "565.38",
                "certificate": "00000001",
                "effective_date": "2020-01-22",
                "interest_disbursement": "Credit acc 003.12345.111222333",
                "interest_payment_frequency": "Semi-annually",
                "interest_rate": "0.04",
                "maturity_date": "2021-01-022",
                "maturity_instructions": "Credit acc 003.12345.111222333",
                "next_interest_payment_date": "2020-07-22",
                "redeemable": "Yes",
                "redemption_rate": "0.04840",
                "term": "1 year"
            }
        }
    }


def test_get_new_gic():
    response = documents.get(
        api_key=API_KEY,
        doc_dc=False,
        doc_type="gic",
        doc_num="new")

    assert response["status"] == 200
    assert response["message"] == "wip"
    assert response["data"] == {
        "doc_type": "gic",
        "doc_num": "",
        "descr": "",
        "acc_num": "",
        "fields": {
            "detail": {
                "anticipated_interest": "",
                "certificate": "",
                "effective_date": "",
                "interest_disbursement": "",
                "interest_payment_frequency": "",
                "interest_rate": "",
                "maturity_date": "",
                "maturity_instructions": "",
                "next_interest_payment_date": "",
                "redeemable": "",
                "redemption_rate": "",
                "term": ""
            }
        }
    }
