""" pytest """

# pylint: disable=missing-function-docstring

from ledger1.reports.reports_service import service as reports
from ledger1.admin import admin

API_KEY: str ="Bearer 2s3d4f-1q2w3e4r5t6y7u8i9o0p"

def test_chart_accounts():
    """ test chart of accunts """

    admin.get(
        api_key=API_KEY,
        param="reset")

    result = reports(
        api_key=API_KEY,
        name="chart_accounts")

    assert isinstance(result, dict)
    assert result["code"] == 200
    assert result["message"] == "ok"
    assert isinstance(result["data"], dict)
    assert result["data"]["header"] == {"entity_name": "Test Ltd.", "title": "chart of accounts"}
    assert isinstance(result["data"]["table"], list)
    assert result["data"]["table"][0] == ['num', 'name', 'Dc']
    assert result["data"]["table"][1] == ["1.0.0", "assets", "D"]


def test_journal():
    """ test chart of accunts """

    result = reports(
        api_key=API_KEY,
        name="journal")

    assert isinstance(result, dict)
    assert result["code"] == 200
    assert result["message"] == "ok"
    assert isinstance(result["data"], dict)
    assert result["data"]["header"]["entity_name"] == "Test Ltd."
    assert result["data"]["header"]["title"] == "journal"
    assert isinstance(result["data"]["table"], list)
    assert result["data"]["table"][0] == ['dt', 'num', 'descr', 'seq', 'acc_num', 'acc_name', 'doc_type', 'doc_num', 'val', 'dc']
    assert result["data"]["table"][1] == ['2020-01-02', 1, 'capital contribution john doe', 1, '1.1.2', 'checking account', '', "", 10000.0, 'D']


def test_general_ledger():
    """ test general ledger """

    result = reports(
        api_key=API_KEY,
        name="general_ledger")

    assert isinstance(result, dict)
    assert result["code"] == 200
    assert result["message"] == "ok"
    assert isinstance(result["data"], dict)
    assert result["data"]["header"] == {"entity_name": "Test Ltd.", "title": "general ledger"}
    assert result["data"]["filters"] == {
        'acc': '1.0.0',
        'acc_to': '9.9.9',
        'date': '2020-01-01',
        'date_to': '2020-01-31'}
    assert  result["data"]["table"][0] == ['dt', 'num', 'descr', 'seq', 'doc_type', 'doc_num', 'val_db', 'val_cr', 'val_bal']
    assert result["data"]["table"][1] == ['1.1.2 - checking account']
    assert result["data"]["table"][2] == ['2020-01-02', 1, 'capital contribution john doe', 1, '', "", 10000.0, 0, 10000.0]


def test_trial_balance():
    """ test trial balance """

    result = reports(
        api_key=API_KEY,
        name="trial_balance")

    assert isinstance(result, dict)
    assert result["code"] == 200
    assert result["message"] == "ok"
    assert result["data"]["header"] == {"entity_name": "Test Ltd.", "title": "trial balance"}
    assert result["data"]["filters"] == {
        'acc': '1.0.0',
        'acc_to': '9.9.9',
        'date': '2020-01-01',
        'date_to': '2020-01-31'}
    assert result["data"]["table"][0] == ['acc_num', 'acc_name', 'val_open', 'val_db', 'val_cr', 'val_bal']
    assert result["data"]["table"][1] == ['1.0.0', 'assets', 0, 22625.0, -1240.0, 21385.0]
    assert result["data"]["table"][2] == ['1.1.0', 'current assets', 0, 22625.0, -1240.0, 21385.0]
    assert result["data"]["table"][3] == ['1.1.1', 'cash', 0, 0, 0, 0]
    assert result["data"]["table"][4] == ['1.1.2', 'checking account', 0, 21050.0, -190.0, 20860.0]
